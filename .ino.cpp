#ifdef __IN_ECLIPSE__
//This is a automatic generated file
//Please do not modify this file
//If you touch this file your change will be overwritten during the next build
//This file has been generated on 2016-05-20 20:46:57

#include "Arduino.h"
#include "Arduino.h"
#include "ArduinoJson.h"
#include "LedControl.h"
#include "UTFT.h"
int joystick_get_x() ;
int joystick_get_y() ;
int joystick_get_z() ;
void setup() ;
void print_lc(LedControl *target, int val) ;
void print_lc_string(LedControl *target, const char *str) ;
void print_lcd1(char *str) ;
void reset_serial_buffer() ;
bool check_message() ;
void wait_for_handshake() ;
void check_for_command() ;
void loop() ;

#include "joystick.ino"


#endif
