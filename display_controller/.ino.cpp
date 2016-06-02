#ifdef __IN_ECLIPSE__
//This is a automatic generated file
//Please do not modify this file
//If you touch this file your change will be overwritten during the next build
//This file has been generated on 2016-06-02 18:44:19

#include "Arduino.h"
#include "Arduino.h"
#include "ArduinoJson.h"
#include "LedControl.h"
#include "UTFT.h"
#include "Wire.h"
void setupLCD( const UTFT &lcd) ;
void setup() ;
void print_lc(LedControl *target, int val) ;
void print_lc_string(LedControl *target, const char *str) ;
void print_lcd1(char *str) ;
void reset_serial_buffer() ;
void dieError(int number) ;
bool check_message() ;
void wait_for_handshake() ;
void check_for_command() ;
void loop() ;

#include "display_controller.ino"


#endif
