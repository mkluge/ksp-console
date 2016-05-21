general setup:
  - KSP with krpc plugin
  - python client on the PC that talks over the USB/Serial port to an arduino
  - on another arduino the arduino: buttons, displays, joysticks, ...

joysticks:
  - 2 with 3 axes each
  - 6 analog ports in total (0-2 and 3-5)
  - 2x GND, 2x 5V
  - one for steering
  - one for translation
  - attached to primary arduino
  
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
  
buttons
  - button that switch a state and light up if enabled
    - RCS
    - SAS
    - Light
    - Gear
    - Brake
    - Reaction Wheels
    - precision mode for the joysticks
    - 7 inputs (7 gnds) and 7 leds (outputs)
  - kerbal buttons
    - run
    - jump
    - grab
    - eva pack toggle (switch type)
    - 4 inputs (4 gnds) and 1 led (output)
  - button that just kick something off
    - 10x for action groups (light up if action group defined)
    - 10 inputs (10 gnds) and 10 leds (outputs)
    - maybe predefine some action groups like solar panels?
    - Stage
    - Abort
    - Undock
    - Checkpoint
    - Load
    - Chute deploy
    - Self test all LEDs?
    - 7 inputs (7 gnds)
    
LCD TFT diplays:
  - show fuel and stuff
  - 2 160x128 panels, 1.8", SPI interface
  - 5 pins each, so 10 digital pins
  - 4x 5V (background LEDs), 4x GND
  - on seconds arduino
  
9-er panel Apollo-style for Warnings and Info:
  - pin?
  - Fuel low
  - RCS fuel low
  - Bat low
  - Temp warn
  - G-Force warn
  - Parachute safe
  - 9 inputs (9 gnds)
