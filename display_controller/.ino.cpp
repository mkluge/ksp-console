#ifdef __IN_ECLIPSE__
//This is a automatic generated file
//Please do not modify this file
//If you touch this file your change will be overwritten during the next build
//This file has been generated on 2016-07-01 22:03:14

#include "Arduino.h"
#include "Arduino.h"
#include "ArduinoJson.h"
#include "UTFT.h"
#include "Wire.h"
#include "../main_controller/ConsoleSetup.h"
void setupLCD( UTFT &lcd) ;
void setup() ;
void print_lcd( UTFT &lcd, int line, const char *str) ;
void print_lcd( UTFT &lcd, int line, int number) ;
void reset_input_buffer() ;
void reset_message_buffer() ;
void dieError(int number) ;
bool check_message() ;
void receiveEvent(int how_many) ;
void wait_for_handshake() ;
void check_for_command() ;
void loop() ;

#include "display_controller.ino"


#endif
