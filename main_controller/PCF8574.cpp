//
//    FILE: PCF8574.cpp
//  AUTHOR: Rob Tillaart
//    DATE: 02-febr-2013
// VERSION: 0.1.02
// PURPOSE: I2C PCF8574 library for Arduino
//     URL:
//
// HISTORY:
// 0.1.02 replaced ints with byte to reduce footprint;
//        added default value for shiftLeft() and shiftRight()
//        renamed status() to lastError();
// 0.1.01 added value(); returns last read 8 bit value (cached);
//        value() does not always reflect the latest state of the pins!
// 0.1.00 initial version
//

#include "PCF8574.h"
#include "Arduino.h"
#include <Wire.h>

PCF8574::PCF8574(int address) {
	this->chip_hw_address = address;
	for (int offset = 0; offset < 8; offset++) {
		connected_buttons[offset] = NULL;
	}
	last_data = 0;
	last_debounced_data = 0;
	last_error = 0;
	last_update = 0;
}

byte PCF8574::getCurrentSignal()
{
	Wire.beginTransmission(chip_hw_address);
	Wire.requestFrom(chip_hw_address, 1);
	int current_data = Wire.read();
	last_error = Wire.endTransmission();
	return current_data;
}

byte PCF8574::updateState() {
	int current_data = getCurrentSignal();
	// was there a change between the last call of this
	// function
	if( last_data != current_data )
	{
		// yes -> reset the timer
		last_update = millis();
	}
	else
	{
		if( millis()-last_update > debounceDelay &&
			last_data != last_debounced_data )
		{
			byte modified_bits = last_debounced_data ^ last_data;
			last_debounced_data = last_data;
			return modified_bits;
		}
	}
	last_data = current_data;
	return false;
}

byte PCF8574::getValue() {
	return last_debounced_data;
}

LightButton *PCF8574::getButtonForPin(short pin) {
	if (pin < 8) {
		return connected_buttons[pin];
	} else {
		return NULL;
	}
}

void PCF8574::setButtonForPin(short pin, LightButton *button) {
	if (pin < 8) {
		connected_buttons[pin] = button;
	}
}

void PCF8574::write(byte value) {
	Wire.beginTransmission(chip_hw_address);
	last_debounced_data = value;
	Wire.write(last_debounced_data);
	last_error = Wire.endTransmission();
}

bool PCF8574::testPin(short pin) {
	return (last_debounced_data & (1 << pin)) > 0;
}

void PCF8574::setPin(short pin, bool value) {
	int data = getCurrentSignal();
	if (value == LOW) {
		data &= ~(1 << pin);
	} else {
		data |= (1 << pin);
	}
	write(data);
}

int PCF8574::lastError() {
	return last_error;
}

long PCF8574::lastUpdate() {
	return last_update;
}
