/*
 * AnalogInput.cpp
 *
 *  Created on: 01.06.2016
 *      Author: mkluge
 */

#include "AnalogInput.h"

AnalogInput::AnalogInput(const char* json_section, int pin, bool get_diff) {
	name = strdup( json_section );
	this->pin = pin;
	last_value = 0;
	reference_value = 0;
	this->get_diff = get_diff;
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
	// if it changed for at least 2%
	if ( abs(val-last_value)>20 )
	{
		if( get_diff )
		{
			root[name] = val-reference_value;
		}
		else
		{
			root[name] = val;
		}
		last_value = val;
	}
}

int AnalogInput::readValue() {
	return analogRead(pin);
}
