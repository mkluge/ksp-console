#ifdef __IN_ECLIPSE__
//This is a automatic generated file
//Please do not modify this file
//If you touch this file your change will be overwritten during the next build
//This file has been generated on 2016-07-01 21:50:57

#include "Arduino.h"
#include "Arduino.h"
#include "ArduinoJson.h"
#include "AnalogInput.h"
#include "ConsoleSetup.h"
#include "LightButton.h"
#include "PCF8574.h"
#include "Wire.h"
#include "LedControl.h"
void setupLC( LedControl &lc ) ;
void testAllButtons(JsonObject& root) ;
void print_lc(LedControl &target, int val) ;
void print_lc_string(LedControl &target, const char *str) ;
void setup() ;
void reset_serial_buffer() ;
bool check_message() ;
void wait_for_handshake() ;
void dieError(int code) 		;
void sendToSlave(JsonObject &message) ;
void check_button_enabled(JsonObject& rj, const char *key, int button_index) ;
void check_for_command() ;
void loop() ;


#include "joystick.ino"

#endif
