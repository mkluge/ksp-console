/*
 * AnalogInput.h
 *
 *  Created on: 01.06.2016
 *      Author: mkluge
 */

#ifndef ANALOGINPUT_H_
#define ANALOGINPUT_H_

#include "Arduino.h"
#include "ArduinoJson.h"

#define CHECK_LOOPS 100

class AnalogInput {
public:
	AnalogInput( const char* json_section, int pin);
	virtual ~AnalogInput();

	void calibrate();
	void readInto( JsonObject& root );

private:
	int readValue();

	int pin;
	long reference_value;
	int last_value;
	char *name;
};

#endif /* ANALOGINPUT_H_ */
