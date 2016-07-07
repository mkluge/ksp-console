#ifdef __IN_ECLIPSE__
//This is a automatic generated file
//Please do not modify this file
//If you touch this file your change will be overwritten during the next build
//This file has been generated on 2016-07-07 21:14:13

#include "Arduino.h"
#include "Arduino.h"
#include "ArduinoJson.h"
#include "Wire.h"
#include "../main_controller/ConsoleSetup.h"
#include <SPI.h>
#include "Ucglib.h"
void setupLCD( Ucglib_ST7735_18x128x160_SWSPI &lcd) ;
void setup() ;
void print_lcd( Ucglib_ST7735_18x128x160_SWSPI &lcd, int line, const char *str) ;
void print_lcd( Ucglib_ST7735_18x128x160_SWSPI &lcd, int line, int number) ;
void reset_input_buffer() ;
void dieError(int number) ;
void receiveEvent(int how_many) ;
void work_on_command() ;
void loop() ;

#include "display_controller.ino"


#endif
