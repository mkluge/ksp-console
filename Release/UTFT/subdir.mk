################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
C:/Users/mkluge/Documents/Arduino/libraries/UTFT/UTFT.cpp 

C_SRCS += \
C:/Users/mkluge/Documents/Arduino/libraries/UTFT/DefaultFonts.c 

C_DEPS += \
./UTFT/DefaultFonts.c.d 

LINK_OBJ += \
./UTFT/DefaultFonts.c.o \
./UTFT/UTFT.cpp.o 

CPP_DEPS += \
./UTFT/UTFT.cpp.d 


# Each subdirectory must supply rules for building sources it contributes
UTFT/DefaultFonts.c.o: C:/Users/mkluge/Documents/Arduino/libraries/UTFT/DefaultFonts.c
	@echo 'Building file: $<'
	@echo 'Starting C compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-gcc" -c -g -Os -std=gnu11 -ffunction-sections -fdata-sections -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\cores\arduino" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\variants\mega" -I"C:\Users\mkluge\Documents\Arduino\libraries\ArduinoJson\include" -I"C:\Users\mkluge\Documents\Arduino\libraries\LedControl\src" -I"C:\Users\mkluge\Documents\Arduino\libraries\UTFT" -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '

UTFT/UTFT.cpp.o: C:/Users/mkluge/Documents/Arduino/libraries/UTFT/UTFT.cpp
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\cores\arduino" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\variants\mega" -I"C:\Users\mkluge\Documents\Arduino\libraries\ArduinoJson\include" -I"C:\Users\mkluge\Documents\Arduino\libraries\LedControl\src" -I"C:\Users\mkluge\Documents\Arduino\libraries\UTFT" -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '


