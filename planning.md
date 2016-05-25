general setup:
  - KSP with krpc plugin
  - python client on the PC that talks over the USB/Serial port to an arduino
  - on another arduino: buttons, displays, joysticks, ...

joysticks:
  - 2 with 3 axes each
  - 6 analog ports in total (0-2 and 3-5)
  - 2x GND, 2x 5V
  - one for steering
  - one for translation
  - attached to primary arduino (latency ...)
  
slider (10K)
  - for thrust
  - 1x GND, 1x 5V
  - one analog port (6)
  - attached to primary arduino

flip switches
  - Enable Stage
  - Enable Abort
  - each one needs an "active" LED
  - 4 ports, 4x GND
  - PCF8754 (number 1)
  
buttons
  - button that switch a state and light up if enabled
    - RCS (green)
    - SAS (green)
    - Light (white)
    - Gear (white)
    - Brake (white)
    - Reaction Wheels (red)
    - precision mode for the joysticks (blue)
    - 7 inputs (7 gnds) and 7 leds (outputs)
    - will become one [PCF8754](https://www.conrad.de/de/schnittstellen-ic-e-a-erweiterungen-texas-instruments-pcf8574n-por-ic-100-khz-pdip-16-1047951.html?sc.queryFromSuggest=true) for the Switches
    - and one for the LEDs, and one UDN as driver 
    - (numbers 2 und 3)
    
  - kerbal buttons
    - run
    - jump
    - grab
    - eva pack toggle (switch type)
    - 4 inputs (4 gnds) and 1 led (output)
    - one more PCF8754 (number 4), and one UDN port as driver
  - button that just kick something off
    - 10x for action groups (light up if action group defined) (10x white)
    - 10 inputs (10 gnds) and 10 leds (outputs), and one UDN as driver 
    - maybe predefine some action groups like solar panels?
    - Stage (green)
    - Abort (red?)
    - Undock (blue)
    - Checkpoint (white)
    - Load (red?)
    - Chute deploy (blue)
    - Self test all LEDs?
    - 7 inputs (7 gnds)
    - one more PCF8754 (number 5)

LCD TFT diplays:
  - show fuel and stuff
  - 2 160x128 panels, 1.8", SPI interface
  - 5 pins each, so 10 digital pins
  - 4x 5V (background LEDs), 4x GND
  - on second arduino (slave)
  - note: connect both CS signals together to one 
  
9-er panel Apollo-style for Warnings and Info:
  - pins per package? voltage?
  - Fuel low
  - RCS fuel low
  - Bat low
  - Temp warn
  - G-Force warn
  - Parachute safe
  - 9 inputs (9 gnds)
  - makes one PCF8754 (number 6)
