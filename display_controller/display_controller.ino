#include "Arduino.h"
#include "ArduinoJson.h"
#include "Wire.h"
#include "../main_controller/ConsoleSetup.h"
#include <SPI.h>
#include "Ucglib.h"

Ucglib_ST7735_18x128x160_SWSPI lcd_right( 1, 2, 3, 0, 4);
Ucglib_ST7735_18x128x160_SWSPI lcd_left( 9, 10, 11, 8, 12);

#define READ_BUFFER_SIZE 200
char read_buffer[READ_BUFFER_SIZE];
int read_buffer_offset = 0;
int empty_buffer_size = 0;
volatile bool have_handshake=false;
volatile bool command_complete=false;

void setupLCD( Ucglib_ST7735_18x128x160_SWSPI &lcd) {
	  lcd.begin(UCG_FONT_MODE_SOLID);
	  lcd.setRotate180();
	  lcd.setColor(0, 255, 255, 255);
	  lcd.setColor(1, 0, 0, 0);
//	  lcd.setColor(2, 0, 120, 0);
//	  lcd.setColor(3, 0, 120, 120);
	  lcd.clearScreen();
}

void setup() {	
	setupLCD( lcd_right );
	setupLCD( lcd_left );

	reset_input_buffer();
	Wire.onReceive(receiveEvent);
	Wire.begin(SLAVE_HW_ADDRESS);
	delay(100);
}

void print_lcd( Ucglib_ST7735_18x128x160_SWSPI &lcd, int line, const char *str) {
	  lcd.setFont(ucg_font_helvR10_hr);
	  lcd.setPrintPos(1,20+line*15);
	  lcd.print(str);
}

void print_lcd( Ucglib_ST7735_18x128x160_SWSPI &lcd, int line, int number) {
	char buf[20];
	sprintf( buf, "%d", number);
	print_lcd( lcd, line, buf);
}

void reset_input_buffer() {
	memset(read_buffer, 0, READ_BUFFER_SIZE);
	read_buffer_offset = 0;
}

void dieError(int number) {
	print_lcd( lcd_left, 0, "Error:");
	print_lcd( lcd_left, 1, number);
	// stay here
	delay(100000);
}

// read the data into the buffer,
// if the current input buffer is not full
void receiveEvent(int how_many) {
	// in case we already have a full command
	// => dump
	if( command_complete )
	{
		while( Wire.available()>0 )
			Wire.read();
		return;
	}
	while( Wire.available()>0 )
	{
		char inByte = Wire.read();
		if ( inByte == 0x00 )
		{
			command_complete = true;
			// dump if there is more one the wire
			while( Wire.available()>0 )
				Wire.read();
			return;
		}
		// otherwise store the current byte
		if (read_buffer_offset < READ_BUFFER_SIZE) {
			read_buffer_offset++;
			read_buffer[read_buffer_offset] = inByte;
		} else {
			read_buffer[READ_BUFFER_SIZE-1]=0;
			command_complete = true;
			return;
		}
	}
}

void work_on_command() {
	StaticJsonBuffer <READ_BUFFER_SIZE> readBuffer;
	JsonObject& rj = readBuffer.parseObject(read_buffer);
	if (!rj.success()) {
		print_lcd( lcd_right, 1, read_buffer);
		dieError(3);
	} else {
		if(!have_handshake)
		{
			if (rj["start"] == 2016) {
				have_handshake = true;
				print_lcd( lcd_left, 2, "Handshake");
				print_lcd( lcd_right, 2, "   ");
				return;
			}
		}
		else
		{
			int speed = rj["speed"];
			print_lcd( lcd_left, 4, speed);
			int height = rj["height"];
			print_lcd( lcd_left, 5, height);
		}
	}
}

void loop() {
	static bool dot_on=false;

	while( 1 )
	{
		if( command_complete )
		{
			work_on_command();
			reset_input_buffer();
			command_complete = false;
		}
		if( !have_handshake )
		{
			if (dot_on == true) {
				print_lcd( lcd_left, 2, "  .");
				print_lcd( lcd_right, 2, "   ");
			} else {
				print_lcd( lcd_right, 2, "  .");
				print_lcd( lcd_left, 2, "   ");
			}
			dot_on = !dot_on;
			delay(100);
		}
	}
}
