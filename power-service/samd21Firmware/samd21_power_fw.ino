/*
  This code run on MCU at91samd21g18, control Power of MPU (Jetson Nano, RPi).

  Arduino Board should select as Seeeduino_Zero.
  TAB size: 8

  Peter Yang 2020-05-12
*/
#include <Wire.h>
#define PIN_RPI_MCU_INT1	8	// PA06
#define PIN_RPI_MCU_INT2	9	// PA07
#define PIN_PWR_DET		2	// PA08
#define PIN_PWR_CONTROL		3	// PA09
#define PIN_IR_PWR_CONTROL	16	// PB09

#define PIN_MCU_FAN_TACH1	4	// PA14
#define PIN_MCU_FAN_PWM1	5	// PA15
#define PIN_MCU_FAN_TACH2	13	// PA17
#define PIN_MCU_FAN_PWM2	11	// PA16

#define PIN_TEMP_ALERT		7	// PA21
#define PIN_TEMP_SDA		20	// PA22
#define PIN_TEMP_SCL		21	// PA23

#define FW_VERSION		"0.2"

#define LOOP_PERIOD		10	/* milliseconds */

int trigger_24v_l = LOW;
int int1_last = LOW;
#define POWER_IR_REG 0X04
#define POWER_ON_IR 0X01
#define POWER_OFF_IR 0X00
/* MPU Power state machine */
enum {
	PW_ST_OFF,

	/* from PWR_CONTROL up to int1 response */
	#define STARTUP_MAX		90 /* seconds */
	PW_ST_STARTUP,

	PW_ST_ON,

	/* from INT2 inform to INT1 response(linux poweroff cmd) */
	#define PRE_OFF_MAX		30 /* seconds */
	PW_ST_PRE_OFF,

	/* from linux poweroff cmd to kernel pm_power_off */
	#define GO_OFF_MAX		16 /* seconds */
	PW_ST_GO_OFF,
};
int pw_state;

enum {
	PW_ACT_NONE = 0,
	PW_ACT_TRIG_UP,
	PW_ACT_TRIG_DOWN,
	PW_ACT_INT1_PULSE,
	PW_ACT_INT1_UP,
};

void setup() {
	/*
	 * Care the INT1 level during MPU Startup.
	 * MPU set pin connected to INT1 as INPUT most time,
	 * so PULLDOWN will set INT1 with a default LOW level input.
	 */
	pinMode(PIN_RPI_MCU_INT1, INPUT_PULLDOWN);
	pinMode(PIN_PWR_DET, INPUT_PULLUP);
	digitalWrite(PIN_RPI_MCU_INT2, LOW);
	pinMode(PIN_RPI_MCU_INT2, OUTPUT);
	digitalWrite(PIN_PWR_CONTROL, LOW);
	pinMode(PIN_PWR_CONTROL, OUTPUT);
	pinMode(PIN_IR_PWR_CONTROL, OUTPUT);
	digitalWrite(PIN_IR_PWR_CONTROL, LOW);
	Wire.begin(4);                // join i2c bus with address #4
	Wire.onReceive(receiveEvent); // register event
	// Open serial communications and wait for port to open:
	Serial.begin(115200);

	/*
	while (!Serial) {
		; // wait for serial port to connect.
		  // Needed for native USB port only
	}
	//*/

	Serial.println("Power Firmware begin v" FW_VERSION);
	Serial.println("Date: " __DATE__);

	pw_state = PW_ST_OFF;
}

// return HIGH, LOW, -1
int smooth_read_trig(void) {
#define SMOOTH_CNT	(160 / LOOP_PERIOD)
	static int history[SMOOTH_CNT] = { -1 };
	int i, v;

	v = digitalRead(PIN_PWR_DET);
	for (i = SMOOTH_CNT - 1; i > 0; i--) {
		history[i] = history[i - 1];
	}
	history[i] = v;

	// -1 means power jitter condition
	for (i = SMOOTH_CNT - 1; i > 0; i--) {
		if (v != history[i]) {
			return -1;
		}
	}
	return v;
}

// return HIGH, LOW, -1
int smooth_read_int1(void) {
#undef SMOOTH_CNT
#define SMOOTH_CNT	3
	static int history[SMOOTH_CNT] = { -1 };
	int i, v;

	v = digitalRead(PIN_RPI_MCU_INT1);
	for (i = SMOOTH_CNT - 1; i > 0; i--) {
		history[i] = history[i - 1];
	}
	history[i] = v;

	// -1 means power jitter condition
	for (i = SMOOTH_CNT - 1; i > 0; i--) {
		if (v != history[i]) {
			return -1;
		}
	}
	return v;
}

int power_do_action(int action, unsigned delta) {
	static unsigned long tm_counter; /* milliseconds */

	if (action == PW_ACT_NONE) {
		// return -1;
	}

	int pw_state_next = pw_state;

	tm_counter += (unsigned long)delta;

	switch (pw_state) {
	case PW_ST_OFF:
		if (action != PW_ACT_TRIG_UP) {
			break;
		}

		/*
		 * 1. If MCU receive the INT3, it will turn on Mosfet
		 * to power up MPU (Jetson Nano or RPi 4).
		 */
		digitalWrite(PIN_RPI_MCU_INT2, LOW);
		digitalWrite(PIN_PWR_CONTROL, HIGH);
		Serial.println("Power up MPU (Jetson Nano, RPi) v" FW_VERSION);
		Serial.println("Date: " __DATE__);

		pw_state_next = PW_ST_STARTUP;
		tm_counter = 0UL;
		break;

	/* from PWR_CONTROL up to int1 response */
	case PW_ST_STARTUP:
		if (action == PW_ACT_INT1_PULSE) {
			pw_state_next = PW_ST_ON;
		} else if (tm_counter >= STARTUP_MAX * 1000UL) {
			/* MPU Startup failed && TIMEOUT */
			digitalWrite(PIN_PWR_CONTROL, LOW);
			delay(1000UL);
			pw_state_next = PW_ST_OFF;
		}
		break;

	case PW_ST_ON:
		
		if (action != PW_ACT_TRIG_DOWN) {
			break;
		}
		/*
		 * 2.If the INT3 disappear, the MCU will send INT2 to MPU.
		 */
		digitalWrite(PIN_RPI_MCU_INT2, HIGH);
		/*
		 * 3.If MPU receive the INT2, it will save data.
		 */
		Serial.println("Inform MPU (Jetson Nano, RPi) to prepare poweroff");

		pw_state_next = PW_ST_PRE_OFF;
		tm_counter = 0UL;
		break;

	/* from INT2 inform to INT1 response(linux poweroff cmd) */
	case PW_ST_PRE_OFF:
		/*
		 * 4.After MPU has saved data, it will send INT1 to
		 *   MCU and turn off the system.
		 */
		if (
		action == PW_ACT_INT1_UP
		||
		/* MPU Application saving data failed && TIMEOUT */
		tm_counter >= PRE_OFF_MAX * 1000UL
		) {
			pw_state_next = PW_ST_GO_OFF;
			tm_counter = 0UL;
			break;
		}
		break;

	/* from linux poweroff cmd to kernel pm_power_off */	
	case PW_ST_GO_OFF:
		if (tm_counter < GO_OFF_MAX * 1000UL) {
			break;
		}
		/*
		 * 5.If MCU receive the INT1, it will turn off Mosfet
		 *   after GO_OFF_MAX sec
		 */
		digitalWrite(PIN_PWR_CONTROL, LOW);
		pw_state_next = PW_ST_OFF;
		tm_counter = 0UL;
		break;
	}

	if (pw_state != pw_state_next) {
		pw_state = pw_state_next;
		Serial.print("New State = ");
		Serial.print((int)pw_state);
		Serial.print(", Timer Counter = ");
		Serial.print(tm_counter);
		Serial.println(" ms");
	}
	return 0;
}

static unsigned millis_l;
void loop() {
	int action = PW_ACT_NONE;

	int int1_stat;
	int1_stat = smooth_read_int1();
	if (int1_stat == HIGH && int1_last == LOW) {
		action = PW_ACT_INT1_UP;
	} else
	if (int1_stat == LOW && int1_last == HIGH) {
		action = PW_ACT_INT1_PULSE;
	}

	int trigger_24v;
	trigger_24v = smooth_read_trig();
	if (pw_state == PW_ST_OFF || pw_state == PW_ST_ON) {
		if (trigger_24v == HIGH /*&& trigger_24v_l == LOW*/) {
			action = PW_ACT_TRIG_UP;
		} else
		if (trigger_24v == LOW /*&& trigger_24v_l == HIGH*/) {
			action = PW_ACT_TRIG_DOWN;
		}
	}

	/* the actual processing */
	unsigned m = millis();
	// long type round
	if (m < millis_l) {
		millis_l = 0;
	}
	power_do_action(action, m - millis_l);
	millis_l = m;

	if (int1_stat >= 0) {
		int1_last = int1_stat;
	}

	// only record meaningful HIGH/LOW
	if (trigger_24v >= 0) {
		trigger_24v_l = trigger_24v;
	}

	delay(LOOP_PERIOD);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany)
{
	if (POWER_IR_REG != Wire.read())
		return;
	if (!Wire.available())
		return;
	digitalWrite(PIN_IR_PWR_CONTROL,Wire.read());
}