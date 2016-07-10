################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
INO_SRCS += \
../joystick.ino 

CPP_SRCS += \
../.ino.cpp \
../AnalogInput.cpp \
../LightButton.cpp \
../PCF8574.cpp 

LINK_OBJ += \
./.ino.cpp.o \
./AnalogInput.cpp.o \
./LightButton.cpp.o \
./PCF8574.cpp.o 

INO_DEPS += \
./joystick.ino.d 

CPP_DEPS += \
./.ino.cpp.d \
./AnalogInput.cpp.d \
./LightButton.cpp.d \
./PCF8574.cpp.d 


# Each subdirectory must supply rules for building sources it contributes
.ino.cpp.o: ../.ino.cpp
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\cores\arduino" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\variants\mega" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire\src" -I"C:\Users\mkluge\Documents\Arduino\libraries\ArduinoJson\include" -I"C:\Users\mkluge\Documents\Arduino\libraries\LedControl\src" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\SPI" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\SPI\src" -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall  -std=c++11
	@echo 'Finished building: $<'
	@echo ' '

AnalogInput.cpp.o: ../AnalogInput.cpp
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\cores\arduino" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\variants\mega" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire\src" -I"C:\Users\mkluge\Documents\Arduino\libraries\ArduinoJson\include" -I"C:\Users\mkluge\Documents\Arduino\libraries\LedControl\src" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\SPI" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\SPI\src" -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall  -std=c++11
	@echo 'Finished building: $<'
	@echo ' '

LightButton.cpp.o: ../LightButton.cpp
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\cores\arduino" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\variants\mega" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire\src" -I"C:\Users\mkluge\Documents\Arduino\libraries\ArduinoJson\include" -I"C:\Users\mkluge\Documents\Arduino\libraries\LedControl\src" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\SPI" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\SPI\src" -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall  -std=c++11
	@echo 'Finished building: $<'
	@echo ' '

PCF8574.cpp.o: ../PCF8574.cpp
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\cores\arduino" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\variants\mega" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire\src" -I"C:\Users\mkluge\Documents\Arduino\libraries\ArduinoJson\include" -I"C:\Users\mkluge\Documents\Arduino\libraries\LedControl\src" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\SPI" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\SPI\src" -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall  -std=c++11
	@echo 'Finished building: $<'
	@echo ' '

joystick.o: ../joystick.ino
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\cores\arduino" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\variants\mega" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire\src" -I"C:\Users\mkluge\Documents\Arduino\libraries\ArduinoJson\include" -I"C:\Users\mkluge\Documents\Arduino\libraries\LedControl\src" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\SPI" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\SPI\src" -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall  -std=c++11
	@echo 'Finished building: $<'
	@echo ' '


