#ifdef __IN_ECLIPSE__
//This is a automatic generated file
//Please do not modify this file
//If you touch this file your change will be overwritten during the next build
//This file has been generated on 2016-06-02 19:18:04

#include "Arduino.h"
#include "Arduino.h"
#include "ArduinoJson.h"
#include "AnalogInput.h"
#include "PCF8754.h"
#include "ConsoleSetup.h"
bool testAllButtons(JsonObject& root) ;
void setup() ;
void reset_serial_buffer() ;
bool check_message() ;
void wait_for_handshake() ;
void sendToSlave(JsonObject& message) ;
void check_button_enabled(JsonObject& root, const char *key, int button_index) ;
void check_for_command() ;
void loop() ;


#include "joystick.ino"

#endif
