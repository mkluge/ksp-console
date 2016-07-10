#include "Arduino.h"
#include "ArduinoJson.h"
#include "AnalogInput.h"
#include "ConsoleSetup.h"
#include "LightButton.h"
#include "PCF8574.h"
#include "Wire.h"
#include "LedControl.h"

LedControl *led_top    = new LedControl(5, 7, 6, 1);
LedControl *led_bottom = new LedControl(10, 12, 11, 1);

AnalogInput *analog_inputs[] = {
		new AnalogInput("yaw", A5, true),
		new AnalogInput("pitch", A6, true),
		new AnalogInput("roll", A7, true),
		new AnalogInput("xtrans", A2, true),
		new AnalogInput("ytrans", A3, true),
		new AnalogInput("ztrans", A1, true),
		new AnalogInput("thrust", A0, false)
};
const int analog_input_count = sizeof(analog_inputs) / sizeof(AnalogInput*);

#define READ_BUFFER_SIZE 200
char read_buffer[READ_BUFFER_SIZE];
unsigned int read_buffer_offset = 0;
int empty_buffer_size = 0;
bool have_handshake = false;

#define PCF_BASE_ADDRESS 0x38

PCF8574 *key_chips[] = {
		new PCF8574(PCF_BASE_ADDRESS + 0),
		new PCF8574(PCF_BASE_ADDRESS + 1),
		new PCF8574(PCF_BASE_ADDRESS + 2),
		new PCF8574(PCF_BASE_ADDRESS + 3),
		new PCF8574(PCF_BASE_ADDRESS + 4),
};

PCF8574 *led_chips[] = {
		new PCF8574(PCF_BASE_ADDRESS + 5),
		new PCF8574(PCF_BASE_ADDRESS + 6),
};

// some button indizes for easier handling
#define STAGE_BUTTON 0
#define RCS_BUTTON 1
#define SAS_BUTTON 2
#define GEAR_BUTTON 3
#define LIGHT_BUTTON 4
#define EVA_PACK_BUTTON 5
#define REACTION_WHEELS_BUTTON 6

LightButton *buttons[] = {
		new LightButton("stage", key_chips[0], 4, led_chips[0], 0),
		new LightButton("rcs", key_chips[0], 5, led_chips[0], 1),
		new LightButton("sas", key_chips[0], 6, led_chips[0], 2)
};

bool interrupt_seen = false;

void setupLC(LedControl *lc)
{
	lc->shutdown(0, false); // turn off power saving, enables display
	lc->setIntensity(0, 15); // sets brightness (0~15 possible values)
	lc->clearDisplay(0); // clear screen
}

void print_led(LedControl *target, long val) {

	int digit = 0;
	bool negative = (val >= 0) ? false : true;
	val = abs(val);
	while (val > 0 && digit < 8)
	{
		int last_digit = val % 10;
		val = val / 10;
		target->setDigit(0, digit, (byte) last_digit, false);
		digit++;
	}
	if (negative && digit<8) {
		target->setChar(0, digit, '-', false);
		digit++;
	}
	while (digit < 8) {
		target->setChar(0, digit, ' ', false);
		digit++;
	}
}

void print_led(LedControl *target, const char *str) {
	int len = strlen(str);
	int digit = 0;
	while (digit < 8 && len > 0) {
		target->setChar(0, digit, str[len - 1], false);
		len--;
		digit++;
	}
}

/**
 * checks all buttons and if anyone changed its state, adds the new state
 * of the botton to the json object
 */
void testAllButtons(JsonObject& root) {
// update chips
	for (auto pcf8754 : key_chips) {
		byte changed_bits;
		if ((changed_bits = pcf8754->updateState()) != 0x00) {
			// test all bits and update the json for each bit set
			int current_bit = 0;
			while (changed_bits != 0) {
				if (changed_bits & (1)) {
					LightButton *button = pcf8754->getButtonForPin(current_bit);
					if( button!=NULL )
					{
						// low active inputs
						root[button->getName()] =
								(pcf8754->testPin(current_bit)==false) ? 1 : 0;
					}
				}
				current_bit++;
				changed_bits >>= 1;
			}
		}
	}
}

void setup() {
	setupLC(led_top);
	setupLC(led_bottom);

	Serial.begin(38400);
	Wire.begin();
	for (auto i : analog_inputs)
	{
		i->calibrate();
	}

	// to act as input, all outputs have to be on HIGH
	for (auto key_chip: key_chips)
	{
		key_chip->write(0xFF);
	}

	// test lamps
	for( auto led_chip: led_chips)
	{
		led_chip->write(0xff);
	}
	print_led(led_top, 88888888);
	print_led(led_bottom, 88888888);
	delay(1000);
	for( auto led_chip: led_chips)
	{
		led_chip->write(0x00);
	}
	print_led(led_top, "        ");
	print_led(led_bottom, "        ");
	// turn off the two leds
	// LED rechts
	key_chips[4]->setPin( 4, 0);
	// LED links
	key_chips[4]->setPin( 5, 0);

	pinMode( 19, INPUT);
	empty_buffer_size = Serial.availableForWrite();
	wait_for_handshake();
	// wait for the i2c slave to initialize
	delay(100);
	print_led(led_top, "--");
	awakeSlave();
	delay(100);
}

void reset_serial_buffer() {
	memset(read_buffer, 0, READ_BUFFER_SIZE);
	read_buffer_offset = 0;
}

/**
 * returns true if buffer contains exactly on line including the "\n"
 * otherwise just stores what is on the serial port and returns false
 */
bool check_message() {
	// always read one full message
	if (Serial.available()) {
		char inByte = 0;
		while (1) {
			// just wait for the rest to show up ..
			while (Serial.available() == 0)
				;
			inByte = Serial.read();
			if (inByte == '\n') {
				read_buffer[read_buffer_offset] = 0;
				return true;
			}
			if (read_buffer_offset < (READ_BUFFER_SIZE - 1)) {
				read_buffer[read_buffer_offset] = inByte;
				read_buffer_offset++;
			} else {
				dieError(3);
			}
		}
	}
	return false;
}

void wait_for_handshake() {
	reset_serial_buffer();
	bool dot_on = true;
	while (true) {
		if (check_message() == false) {
			if (dot_on == true) {
				print_led(led_top, "   .");
				print_led(led_bottom, "    ");
			} else {
				print_led(led_top, "    ");
				print_led(led_bottom, "   .");
			}
			dot_on = !dot_on;
			delay(1000);
		} else {
			StaticJsonBuffer<READ_BUFFER_SIZE> sjb;
			JsonObject& rj = sjb.parseObject(read_buffer);
			// the only way to get this thing going
			if (rj.success() && rj["start"] == 2016) {
				have_handshake = true;
				return;
			}
			reset_serial_buffer();
		}
	}
}

void dieError(int code)
		{
	print_led(led_top, "E");
	print_led(led_top, code);
}

void sendToSlave(JsonObject &message) {
	char buf[200];
	memset(buf, 0, 200);
	message.printTo(buf, 200);
	buf[198]=0;
	Wire.beginTransmission(SLAVE_HW_ADDRESS);
	Wire.write(buf);
	Wire.write('\n');
	Wire.endTransmission();
}

void check_button_enabled(JsonObject& rj, const char *key, int button_index) {
	if (rj.containsKey(key)) {
		bool state = (rj[key] == 1) ? true : false;
		buttons[button_index]->setLight(state);
		rj.remove(key);
	}
}

void check_for_command() {
	if (check_message() == true) {
		StaticJsonBuffer<READ_BUFFER_SIZE> readBuffer;
		JsonObject& rj = readBuffer.parseObject(read_buffer);

		// Lesen, was für hier dabei ist
		if (!rj.success()) {
			dieError(2);
		} else {
			check_button_enabled(rj, "rcs", RCS_BUTTON);
			check_button_enabled(rj, "sas", SAS_BUTTON);
			check_button_enabled(rj, "gear", GEAR_BUTTON);
			check_button_enabled(rj, "light", LIGHT_BUTTON);
			check_button_enabled(rj, "eva_backpack", EVA_PACK_BUTTON);
			check_button_enabled(rj, "reaction_wheels", REACTION_WHEELS_BUTTON);

			// wenn noch lang genug -> display controller
			if (rj.size() > 0) {
				sendToSlave(rj);
			}
		}
		reset_serial_buffer();
	}
}

void awakeSlave()
{
	StaticJsonBuffer<READ_BUFFER_SIZE> buffer;
	JsonObject& rj = buffer.createObject();
	rj["start"] = 2016;
	sendToSlave(rj);
}

void loop()
{
	StaticJsonBuffer<400> writeBuffer;
	JsonObject& root = writeBuffer.createObject();
	for (auto i: analog_inputs)
	{
		i->readInto(root);
	}

	testAllButtons(root);
	// if we have data and can send (nothing is in the buffer)
	if (root.size() > 0 && (Serial.availableForWrite() == empty_buffer_size)) {
		root.printTo(Serial);
		Serial.print('\n');
		Serial.flush();
	}
	check_for_command();
}
