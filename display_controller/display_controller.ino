#include "Arduino.h"
#include "ArduinoJson.h"
#include "LedControl.h"
#include "UTFT.h"
#include "Wire.h"

// Declare which fonts we will be using
//extern uint8_t SmallFont[];
extern uint8_t BigFont[];
//extern uint8_t SevenSegNumFont[];

// Belegung für braun = 21
/*
 #define SCLK 17
 #define MOSI 18
 #define CS   21
 #define DC   19
 #define RESET 20
 */
// Belegung für braun = 52
#define SCLK 44
#define MOSI 46
#define CS   52
#define DC   48
#define RESET 50

//UTFT(Model, SDA, SCL, CS, RST[, RS]);
UTFT lcd1(ST7735, MOSI1, SCLK1, CS1, RESET1, DC1);
UTFT lcd2(ST7735, MOSI2, SCLK2, CS2, RESET2, DC2);

#define READ_BUFFER_SIZE 200
char read_buffer[READ_BUFFER_SIZE];
int read_buffer_offset = 0;
int empty_buffer_size = 0;

// constructor args are: DIN, CLK, CS, #CHIPS
LedControl lc1 = LedControl(4, 3, 2, 1);
LedControl lc2 = LedControl(7, 6, 5, 1);

void setupLCD( const UTFT &lcd) {
	lcd.InitLCD(PORTRAIT);
	lcd.clrScr();
	lcd.setColor(200, 255, 200); // red, green, blue
	lcd.setBackColor(0, 0, 0);
	lcd.setFont(BigFont); // Allows 15 rows of 20 characters
}

void setup() {
	Wire.begin(SLAVE_HW_ADDRESS);

	setupLCD( lcd1 );
	setupLCD( lcd2 );

	lc1.shutdown(0, false); // turn off power saving, enables display
	lc1.setIntensity(0, 15); // sets brightness (0~15 possible values)
	lc1.clearDisplay(0); // clear screen
	lc2.shutdown(0, false); // turn off power saving, enables display
	lc2.setIntensity(0, 15); // sets brightness (0~15 possible values)
	lc2.clearDisplay(0); // clear screen
}

void print_lc(LedControl *target, int val) {
	if (target == NULL) {
		return;
	}
	int digit = 0;
	bool negative = (val >= 0) ? false : true;
	val = abs(val);
	while (val > 0 && digit < 8) {
		int last_digit = val % 10;
		val = val / 10;
		target->setDigit(0, digit, (byte) last_digit, false);
		digit++;
	}
	if (negative) {
		target->setChar(0, digit, '-', false);
		digit++;
	}
	while (digit < 8) {
		target->setChar(0, digit, ' ', false);
		digit++;
	}
}

void print_lc_string(LedControl *target, const char *str) {
	int len = strlen(str);
	int digit = 0;
	while (digit < 8 && len > 0) {
		target->setChar(0, digit, str[len - 1], false);
		len--;
		digit++;
	}
}

void print_lcd1(char *str) {
	myGLCD.print(str, LEFT, 0);
}

void reset_serial_buffer() {
	memset(read_buffer, 0, READ_BUFFER_SIZE);
	read_buffer_offset = 0;
}

void dieError(int number) {
	char buf[10];
	sprint(buf, "%8d", number)
	print_lc_string(&lc1, "       E");
	print_lc_string(&lc2, buf);
// keep hanging around
	while (true) {
	};
}

/**
 * returns true if buffer contains exactly on line including the "\n"
 * otherwise just stores what is on the serial port and returns false
 */
bool check_message() {
// always read one full message
	if (Wire.available()) {
		char inByte = 0;
		while (1) {
			// just wait for the rest to show up ..
			while (While.available() == 0)
				;
			inByte = Wire.read();
			if (inByte == '\n') {
				read_buffer[read_buffer_offset] = 0;
				return true;
			}
			if (read_buffer_offset < (READ_BUFFER_SIZE - 1)) {
				read_buffer[read_buffer_offset] = inByte;
				read_buffer_offset++;
			} else {
				dieError(1);
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
				print_lc_string(&lc1, "        ");
				print_lc_string(&lc2, "........");
			} else {
				print_lc_string(&lc1, "........");
				print_lc_string(&lc2, "        ");
			}
			dot_on = !dot_on;
			delay(1000);
		} else {
			StaticJsonBuffer < READ_BUFFER_SIZE > readBuffer;
			JsonObject& rj = readBuffer.parseObject(read_buffer);
			// the only way to get this thing going
			if (rj.success() && rj["start"] == 2016) {
				print_lc_string(&lc1, "       -");
				print_lc_string(&lc2, "       -");
				reset_serial_buffer();
				return;
			}
			reset_serial_buffer();
		}
	}
}

void check_for_command() {
	if (check_message() == true) {
		StaticJsonBuffer < READ_BUFFER_SIZE > readBuffer;
		JsonObject& rj = readBuffer.parseObject(read_buffer);

		if (!rj.success()) {
			print_lc_string(&lc1, "E");
			print_lc(&lc2, 3);
		} else {
			char buff[20];
			memset(buff, 0, 20);
			int speed = rj["speed"];
			print_lc(&lc1, speed);
			int height = rj["height"];
			print_lc(&lc2, height);
//			snprintf( buff, 15, "%8d", height);
//			print_lcd1(buff);
		}
		reset_serial_buffer();
	}
}

void loop() {
// main loop
	check_for_command();
}
