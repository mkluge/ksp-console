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

bool write_in_progress = false;
#define READ_BUFFER_SIZE 200
char read_buffer[READ_BUFFER_SIZE];
int read_buffer_offset = 0;
int empty_buffer_size = 0;
int complete_message_length = 0;

void setupLCD( UTFT &lcd) {
	lcd.InitLCD(PORTRAIT);
	lcd.clrScr();
	lcd.setColor(200, 255, 200);
	lcd.setBackColor(0, 0, 0);
	lcd.setFont(SmallFont); // 20 rows; 15 characters
	lcd.clrScr();
}

void setup() {

	setupLCD( lcd_right );
	setupLCD( lcd_left );

	reset_input_buffer();
	reset_message_buffer();
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

void reset_message_buffer() {
	memset(complete_message, 0, READ_BUFFER_SIZE);
	complete_message_length = 0;
}

void dieError(int number) {
	print_lcd( lcd_left, 0, "Error");
	print_lcd( lcd_left, 1, number);
	// stay here
	while (true) {
	};
}

bool check_message() {
	if( write_in_progress )
		return false;
	if( complete_message[complete_message_length]=='\n' ) {
		complete_message_length--;
		complete_message[complete_message_length] = 0;
		return true;
	}
	return false;
}

// read the data into the buffer,
// if the current input buffer is not full
void receiveEvent(int how_many) {
	write_in_progress = true;
	while( Wire.available()>0 )
	{
		char inByte = Wire.read();
		// just continue and dump the byte if
		// we already have a complete buffer and
		// wait for the app to finish working on the
		// last one ...
		if( read_buffer_offset>0 &&
			read_buffer[read_buffer_offset-1] == '\n' )
		{
			continue;
		}
		// otherwise store the current byte
		if (read_buffer_offset < READ_BUFFER_SIZE) {
			read_buffer_offset++;
			read_buffer[read_buffer_offset] = inByte;
		} else {
			print_lcd( lcd_right, 0, read_buffer);
			dieError(read_buffer_offset);
		}
		if ( inByte == '\n' )
				break;
	}
	// if there is a complete message and the
	// app says it is done with working on the
	// last message by setting complete_message[0] to 0
	// we copy the current message over and reset
	// the input buffer
	if( complete_message[0]==0 &&
		read_buffer[read_buffer_offset] == '\n')
	{
		read_buffer[read_buffer_offset+1] = 0;
		strncpy( complete_message, read_buffer, READ_BUFFER_SIZE);
		reset_input_buffer();
		complete_message_length = strlen( complete_message )-1;
	}
}

void wait_for_handshake() {
	bool dot_on = true;
	while (true) {
		if (check_message() == false) {
			if (dot_on == true) {
				print_lcd( lcd_left, 2, ".");
				print_lcd( lcd_right, 2, " ");
			} else {
				print_lcd( lcd_right, 2, ".");
				print_lcd( lcd_left, 2, " ");
			}
			dot_on = !dot_on;
			delay(900);
		} else {
			print_lcd( lcd_left, 2, " ");
			print_lcd( lcd_right, 2, " ");
			StaticJsonBuffer <READ_BUFFER_SIZE> readBuffer;
			JsonObject& rj = readBuffer.parseObject(complete_message);
			// the only way to get this thing going
			if (rj.success() && rj["start"] == 2016) {
				print_lcd( lcd_left, 1, " OK ");
				reset_message_buffer();
				return;
			}
			reset_message_buffer();
		}
	}
}

void check_for_command() {
	if (check_message() == true) {
		StaticJsonBuffer <READ_BUFFER_SIZE> readBuffer;
		JsonObject& rj = readBuffer.parseObject(complete_message);
		reset_message_buffer();
		if (!rj.success()) {
			dieError(3);
		} else {
/*			char buff[20];
			memset(buff, 0, 20);
			int speed = rj["speed"];
			print_lc( lc_top, speed);
			int height = rj["height"];
			print_lc( lc_bottom, height);*/
		}
	}
}

void loop() {
// main loop
	wait_for_handshake();
	while ( 1 )
		check_for_command();
}