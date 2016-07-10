/*
 * LightButton.h
 *
 *  Created on: 01.06.2016
 *      Author: mkluge
 */

#ifndef LIGHTBUTTON_H_
#define LIGHTBUTTON_H_

#include "Arduino.h"
#include "PCF8574.h"

class LightButton {
public:
	LightButton( const char *name,
			PCF8574 *i2c_button_chip,
			int i2c_button_chip_pin,
			PCF8574 *i2c_light_chip_address,
			int i2c_light_chip_pin);
	virtual ~LightButton();
	void setLight( bool enable);
	const char *getName() const;
	bool readState() const;

private:
	const char *name;
	PCF8574 *button_chip;
	int button_pin;
	PCF8574 *light_chip;
	int light_pin;
};

#endif /* LIGHTBUTTON_H_ */
