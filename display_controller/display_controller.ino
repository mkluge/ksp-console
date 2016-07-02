#include "Arduino.h"
#include "ArduinoJson.h"
#include "UTFT.h"
#include "Wire.h"
#include "../main_controller/ConsoleSetup.h"

// declare font
extern uint8_t SmallFont[];

//UTFT(Model, SDA, SCL, CS, RST[, RS]);
UTFT lcd_right(ST7735, 2,1,0,4,3);
UTFT lcd_left(ST7735, 10,9,8,12,11);

#define READ_BUFFER_SIZE 200
char read_buffer[READ_BUFFER_SIZE];
int read_buffer_offset = 0;
int empty_buffer_size = 0;
volatile bool have_handshake=false;

void setupLCD( UTFT &lcd) {
	lcd.InitLCD(PORTRAIT);
	lcd.clrScr();
	lcd.setColor(200, 255, 200);
	lcd.setBackColor(0, 0, 0);
	lcd.setFont(SmallFont); // 20 rows; 15 characters
}

void setup() {	
	setupLCD( lcd_right );
	setupLCD( lcd_left );

	reset_input_buffer();
	Wire.onReceive(receiveEvent);
	Wire.begin(SLAVE_HW_ADDRESS);
}

void print_lcd( UTFT &lcd, int line, const char *str) {
	lcd.print( str, LEFT, line*10);
}

void print_lcd( UTFT &lcd, int line, int number) {
	char buf[20];
	sprintf( buf, "%d", number);
	print_lcd( lcd, line, buf);
}

void reset_input_buffer() {
	memset(read_buffer, 0, READ_BUFFER_SIZE);
	read_buffer_offset = 0;
}

void dieError(int number) {
	print_lcd( lcd_left, 0, "Error");
	print_lcd( lcd_left, 1, number);
	// stay here
	while (true) {
	};
}

// read the data into the buffer,
// if the current input buffer is not full
void receiveEvent(int how_many) {
	while( Wire.available()>0 )
	{
		char inByte = Wire.read();
		if ( inByte == '\n' )
		{
			workOnCommand();
			reset_message_buffer();
		}
		// otherwise store the current byte
		if (read_buffer_offset < READ_BUFFER_SIZE) {
			read_buffer_offset++;
			read_buffer[read_buffer_offset] = inByte;
		} else {
			dieError(read_buffer_offset);
		}
	}
}

void wait_for_handshake() {
	while (!have_handshake) {
		if (dot_on == true) {
			print_lcd( lcd_left, 2, ".");
			print_lcd( lcd_right, 2, " ");
		} else {
			print_lcd( lcd_right, 2, ".");
			print_lcd( lcd_left, 2, " ");
		}
		dot_on = !dot_on;
		delay(1000);
	}
}

void work_on_command() {
	StaticJsonBuffer <READ_BUFFER_SIZE> readBuffer;
	JsonObject& rj = readBuffer.parseObject(read_buffer);
	if (!rj.success()) {
		dieError(3);
	} else {
		if(!have_handshake)
		{
			if (rj["start"] == 2016) {
				have_handshake=1;
				print_lcd( lcd_left, 2, " ");
				print_lcd( lcd_right, 2, " ");
				return;
			}
			int speed = rj["speed"];
			print_lcd( lcd_left, speed);
			int height = rj["height"];
			print_lcd( lcd_right, height);
		}
	}
}

void loop() {
	wait_for_handshake();
	while( 1 )
		delay(1000);
}