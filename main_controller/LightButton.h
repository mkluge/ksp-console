/*
 * LightButton.h
 *
 *  Created on: 01.06.2016
 *      Author: mkluge
 */

#ifndef LIGHTBUTTON_H_
#define LIGHTBUTTON_H_

#include "../ksp-console/PCF8754.h"

class LightButton {
public:
	LightButton( const char *name,
			const PCF8754 &i2c_button_chip,
			int i2c_button_chip_pin,
			const PCF8754 &i2c_light_chip_address,
			int i2c_light_chip_pin);
	virtual ~LightButton();
	void setLight( bool enable);
	const char *getName();
	bool readState();

private:
	const PCF8754 &button_chip;
	int button_pin;
	const PCF8754 &light_chip;
	int light_pin;
};

#endif /* LIGHTBUTTON_H_ */
