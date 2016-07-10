#ifdef __IN_ECLIPSE__
//This is a automatic generated file
//Please do not modify this file
//If you touch this file your change will be overwritten during the next build
//This file has been generated on 2016-07-10 22:01:41

#include "Arduino.h"
#include "Arduino.h"
#include "ArduinoJson.h"
#include "AnalogInput.h"
#include "ConsoleSetup.h"
#include "LightButton.h"
#include "PCF8574.h"
#include "Wire.h"
#include "LedControl.h"
void setupLC(LedControl *lc) ;
void print_led(LedControl *target, long val) ;
void print_led(LedControl *target, const char *str) ;
void testAllButtons(JsonObject& root) ;
void setup() ;
void reset_serial_buffer() ;
bool check_message() ;
void wait_for_handshake() ;
void dieError(int code) 		;
void sendToSlave(JsonObject &message) ;
void check_button_enabled(JsonObject& rj, const char *key, int button_index) ;
void check_for_command() ;
void awakeSlave() ;
void loop() ;


#include "joystick.ino"

#endif
