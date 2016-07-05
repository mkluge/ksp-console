#ifdef __IN_ECLIPSE__
//This is a automatic generated file
//Please do not modify this file
//If you touch this file your change will be overwritten during the next build
//This file has been generated on 2016-07-05 21:27:12

#include "Arduino.h"
#include "Arduino.h"
#include "ArduinoJson.h"
#include "Wire.h"
#include "../main_controller/ConsoleSetup.h"
#include <SPI.h>
#include "Ucglib.h"
void setupLCD( LCD_Type &lcd) ;
void setup() ;
void print_lcd( LCD_Type &lcd, int line, const char *str) ;
void print_lcd( LCD_Type &lcd, int line, int number) ;
void reset_input_buffer() ;
void dieError(int number) ;
void receiveEvent(int how_many) ;
void wait_for_handshake() ;
void work_on_command() ;
void loop() ;

#include "display_controller.ino"


#endif
