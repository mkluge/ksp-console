#include "Arduino.h"
#include "ArduinoJson.h"
#include "LedControl.h"
#include "UTFT.h"

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
UTFT myGLCD(ST7735, MOSI, SCLK, CS, RESET, DC);

long x_ref = 0;
long y_ref = 0;
long z_ref = 0;

int last_joy_x = 0;
int last_joy_y = 0;
int last_joy_z = 0;

int joy_x_pin = 2;
int joy_y_pin = 1;
int joy_z_pin = 0;

int count = 0;

#define CHECK_LOOPS 100
#define READ_BUFFER_SIZE 200
char read_buffer[READ_BUFFER_SIZE];
int read_buffer_offset = 0;
int empty_buffer_size = 0;

// constructor args are: DIN, CLK, CS, #CHIPS
LedControl lc1 = LedControl(4, 3, 2, 1);
LedControl lc2 = LedControl(7, 6, 5, 1);

int joystick_get_x()
{
	return analogRead(joy_x_pin);
}

int joystick_get_y()
{
	return analogRead(joy_y_pin);
}

int joystick_get_z()
{
	return analogRead(joy_z_pin);
}

void setup()
{
	Serial.begin(38400);

	myGLCD.InitLCD(LANDSCAPE);
	myGLCD.clrScr();
	myGLCD.setColor(200, 255, 200); // red, green, blue
	myGLCD.setBackColor(0, 0, 0);
	myGLCD.setFont(BigFont); // Allows 15 rows of 20 characters

	lc1.shutdown(0, false); // turn off power saving, enables display
	lc1.setIntensity(0, 15); // sets brightness (0~15 possible values)
	lc1.clearDisplay(0); // clear screen
	lc2.shutdown(0, false); // turn off power saving, enables display
	lc2.setIntensity(0, 15); // sets brightness (0~15 possible values)
	lc2.clearDisplay(0); // clear screen
	/*
	 pinMode(joy_x_pin, INPUT);
	 pinMode(joy_y_pin, INPUT);
	 pinMode(joy_z_pin, INPUT);
	 */
	for (int l = 0; l < CHECK_LOOPS; l++)
	{
		x_ref += joystick_get_x();
		y_ref += joystick_get_y();
		z_ref += joystick_get_z();
	}
	x_ref /= CHECK_LOOPS;
	y_ref /= CHECK_LOOPS;
	z_ref /= CHECK_LOOPS;
	last_joy_x = x_ref;
	last_joy_y = y_ref;
	last_joy_z = z_ref;

	empty_buffer_size = Serial.availableForWrite();
	wait_for_handshake();
}

void print_lc(LedControl *target, int val)
{
	if (target == NULL)
	{
		return;
	}
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
	if (negative)
	{
		target->setChar(0, digit, '-', false);
		digit++;
	}
	while (digit < 8)
	{
		target->setChar(0, digit, ' ', false);
		digit++;
	}
}

void print_lc_string(LedControl *target, const char *str)
{
	int len = strlen(str);
	int digit = 0;
	while (digit < 8 && len > 0)
	{
		target->setChar(0, digit, str[len - 1], false);
		len--;
		digit++;
	}
}

void print_lcd1(char *str)
{
	myGLCD.print( str, LEFT, 0);
}

void reset_serial_buffer()
{
	memset(read_buffer, 0, READ_BUFFER_SIZE);
	read_buffer_offset = 0;
}

/**
 * returns true if buffer contains exactly on line including the "\n"
 * otherwise just stores what is on the serial port and returns false
 */
bool check_message()
{
	while (Serial.available() > 0)
	{
		char inByte = Serial.read();
		if (inByte == '\n')
		{
			read_buffer[read_buffer_offset] = 0;
			return true;
		}
		if (read_buffer_offset < (READ_BUFFER_SIZE - 1))
		{
			read_buffer[read_buffer_offset] = inByte;
			read_buffer_offset++;
		}
		else
		{
			// not supposed to happen!
			print_lc(&lc1, 123);
			print_lc(&lc2, 123);
			// keep hanging around
			while ( true)
			{
			};
		}
	}
	return false;
}

void wait_for_handshake()
{
	reset_serial_buffer();
	bool dot_on = true;
	while ( true)
	{
		if (check_message() == false)
		{
			if (dot_on == true)
			{
				print_lc_string(&lc1, "        ");
				print_lc_string(&lc2, "........");
			}
			else
			{
				print_lc_string(&lc1, "........");
				print_lc_string(&lc2, "        ");
			}
			dot_on = !dot_on;
			delay(1000);
		}
		else
		{
			StaticJsonBuffer<READ_BUFFER_SIZE> readBuffer;
			JsonObject& rj = readBuffer.parseObject(read_buffer);
			// the only way to get this thing going
			if (rj.success() && rj["start"] == 2016)
			{
				print_lc_string(&lc1, "       -");
				print_lc_string(&lc2, "       -");
				reset_serial_buffer();
				return;
			}
			reset_serial_buffer();
		}
	}
}

void check_for_command()
{
	if (check_message() == true)
	{
		StaticJsonBuffer<READ_BUFFER_SIZE> readBuffer;
		JsonObject& rj = readBuffer.parseObject(read_buffer);

		if (!rj.success())
		{
			print_lc_string(&lc1, "E");
			print_lc_string(&lc2, "E");
		}
		else
		{
			char buff[20];
			memset( buff, 0, 20);
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

void loop()
{
	// main loop
	while ( true)
	{
		StaticJsonBuffer<400> writeBuffer;
		JsonObject& root = writeBuffer.createObject();
		int val = joystick_get_x() - x_ref;
		if (val != last_joy_x)
		{
			last_joy_x = val;
			root["yaw"] = val;
		}
		val = joystick_get_y() - y_ref;
		if (val != last_joy_y)
		{
			last_joy_y = val;
			root["pitch"] = val;
		}
		val = joystick_get_z() - z_ref;
		if (val != last_joy_z)
		{
			last_joy_z = val;
			root["roll"] = val;
		}

		// if we have data and can send (nothing is in the buffer)
		if (root.size() > 0
				&& (Serial.availableForWrite() == empty_buffer_size))
		{
			root.printTo(Serial);
			Serial.println("");
			Serial.flush();
		}

		check_for_command();
	}
}
