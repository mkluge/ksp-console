/*
 * LightButtons.cpp
 *
 *  Created on: 01.06.2016
 *      Author: mkluge
 */

#include "LightButton.h"

LightButton::LightButton(const char* name, const PCF8754& i2c_button_chip,
		int i2c_button_chip_pin, const PCF8754& i2c_light_chip_address,
		int i2c_light_chip_pin) {
	button_chip = i2c_button_chip;
	button_pin = i2c_button_chip_pin;
	light_chip = i2c_light_chip;
	light_pin = i2c_light_chip_pin;
	button_chip.setButtonForPin(button_pin, this);
}

LightButton::~LightButton() {
	button_chip.setButtonForPin(button_pin, NULL);
}

void LightButton::setLight(bool enable) {
	light_chip.setPin(light_pin);
}

bool LightButton::readState() {
	return button_chip.testPin(button_pin);
}

