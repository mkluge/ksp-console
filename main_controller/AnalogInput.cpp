/*
 * AnalogInput.cpp
 *
 *  Created on: 01.06.2016
 *      Author: mkluge
 */

#include "AnalogInput.h"

AnalogInput::AnalogInput(const char* json_section, int pin) {
	strdup( json_section, name);
	this->pin = pin;
}

AnalogInput::~AnalogInput() {
	free(name);
}

void AnalogInput::calibrate() {

	reference_value = 0;
	for (int l = 0; l < CHECK_LOOPS; l++)
	{
		reference_value += readValue();
	}
	reference_value /= CHECK_LOOPS;
	last_value = reference_value;
}

void AnalogInput::readInto(JsonObject& root) {
	int val = readValue();
	if ( val!= last_value )
	{
		root[name] = val;
	}
}

int AnalogInput::readValue() {
	return analogRead(pin);
}
