#include "Arduino.h"
#include "ArduinoJson.h"
#include "AnalogInput.h"
#include "ConsoleSetup.h"
#include "LightButton.h"
#include "PCF8574.h"
#include "Wire.h"

const AnalogInput analog_inputs[] = {
		AnalogInput("yaw", 2),
		AnalogInput("pitch", 1),
		AnalogInput("roll", 0),
		AnalogInput("thrust", 3)
};
int analog_input_count = sizeof(analog_inputs) / sizeof(AnalogInput);

#define READ_BUFFER_SIZE 200
char read_buffer[READ_BUFFER_SIZE];
int read_buffer_offset = 0;
int empty_buffer_size = 0;

PCF8574 key_chips[] = {
		PCF8574(0x038),
		PCF8574(0x039),
		PCF8574(0x040),
		PCF8574(0x041)
};

PCF8574 led_chips[] = {
		PCF8574(0x042),
		PCF8574(0x043)
};

// some button indizes for easier handling
#define STAGE_BUTTON 0
#define RCS_BUTTON 1
#define SAS_BUTTON 2
#define GEAR_BUTTON 3
#define LIGHT_BUTTON 4
#define EVA_PACK_BUTTON 5
#define REACTION_WHEELS_BUTTON 6

LightButton buttons[] = {
		LightButton("stage", key_chips[0], 1, nullptr, 0),
		LightButton("rcs", key_chips[0], 2, &led_chips[0], 1)
};

bool interrupt_seen = false;

/**
 * checks all buttons and if anyone changed its state, adds the new state
 * of the botton to the json object
 */
void testAllButtons(JsonObject& root) {
// update chips
	for (auto pcf8754 : key_chips) {
		byte changed_bits;
		if ((changed_bits = pcf8754.updateState()) == true) {
			// test all bits and update the json for each bit set
			int current_bit = 0;
			while (changed_bits != 0) {
				if (changed_bits & (1)) {
					LightButton *button = pcf8754.getButtonForPin(current_bit);
					root[button->getName()] = pcf8754.testPin(current_bit);
				}
				current_bit++;
				changed_bits >>= 1;
			}
		}
	}
}

void setup() {
	Serial.begin(38400);

	for (auto i : analog_inputs)
	{
		i.calibrate();
	}

	empty_buffer_size = Serial.availableForWrite();
	wait_for_handshake();
//	attachInterrupt( 2 );
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
			StaticJsonBuffer<READ_BUFFER_SIZE> readBuffer;
			JsonObject& rj = readBuffer.createObject();
			if (dot_on == true) {
				rj["init"] = 0;
				sendToSlave(rj);
			} else {
				rj["init"] = 1;
				sendToSlave(rj);
			}
			dot_on = !dot_on;
			delay(1000);
		} else {
			StaticJsonBuffer<READ_BUFFER_SIZE> readBuffer;
			JsonObject& rj = readBuffer.parseObject(read_buffer);
			// the only way to get this thing going
			if (rj.success() && rj["start"] == 2016) {
				rj["init"] = 2;
				sendToSlave(rj);
				return;
			}
			reset_serial_buffer();
		}
	}
}

void dieError(int code)
		{
	StaticJsonBuffer<READ_BUFFER_SIZE> buffer;
	JsonObject& rj = buffer.createObject();
	rj["error"] = code;
	sendToSlave(rj);
	delay(5000);
	while (1)
		;
}

void sendToSlave(JsonObject& message) {
	Wire.beginTransmission(SLAVE_HW_ADDRESS);
	message.printTo(Wire);
	Wire.write('\n');
	Wire.endTransmission();
}

void check_button_enabled(JsonObject& rj, const char *key, int button_index) {
	if (rj.containsKey(key)) {
		bool state = (rj[key] == 1) ? true : false;
		buttons[button_index].setLight(state);
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

void loop() {
	StaticJsonBuffer<400> writeBuffer;
	JsonObject& root = writeBuffer.createObject();
	for (auto i : analog_inputs)
	{
		i.readInto(root);
	}

	if (interrupt_seen == true) {
		testAllButtons(root);
		interrupt_seen = false;
	}

	// if we have data and can send (nothing is in the buffer)
	if (root.size() > 0 && (Serial.availableForWrite() == empty_buffer_size)) {
		root.printTo(Serial);
		Serial.println("");
		Serial.flush();
	}

	check_for_command();
}
