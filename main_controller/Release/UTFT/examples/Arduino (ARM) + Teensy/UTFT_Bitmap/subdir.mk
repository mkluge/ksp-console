################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
INO_SRCS += \
C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/UTFT_Bitmap.ino 

C_SRCS += \
C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/icon.c \
C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/info.c \
C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/tux.c 

C_DEPS += \
./UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/icon.c.d \
./UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/info.c.d \
./UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/tux.c.d 

LINK_OBJ += \
./UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/icon.c.o \
./UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/info.c.o \
./UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/tux.c.o 

INO_DEPS += \
./UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/UTFT_Bitmap.ino.d 


# Each subdirectory must supply rules for building sources it contributes
UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/UTFT_Bitmap.o: C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/UTFT_Bitmap.ino
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -MMD -MP -MF"UTFT/examples/Arduino (ARM) + Teensy/UTFT_Bitmap/UTFT_Bitmap.ino.d" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '

UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/icon.c.o: C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/icon.c
	@echo 'Building file: $<'
	@echo 'Starting C compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-gcc" -c -g -Os -std=gnu11 -ffunction-sections -fdata-sections -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -MMD -MP -MF"UTFT/examples/Arduino (ARM) + Teensy/UTFT_Bitmap/icon.c.d" -MT"$@" -D__IN_ECLIPSE__=1 "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '

UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/info.c.o: C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/info.c
	@echo 'Building file: $<'
	@echo 'Starting C compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-gcc" -c -g -Os -std=gnu11 -ffunction-sections -fdata-sections -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -MMD -MP -MF"UTFT/examples/Arduino (ARM) + Teensy/UTFT_Bitmap/info.c.d" -MT"$@" -D__IN_ECLIPSE__=1 "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '

UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/tux.c.o: C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/Arduino\ (ARM)\ +\ Teensy/UTFT_Bitmap/tux.c
	@echo 'Building file: $<'
	@echo 'Starting C compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-gcc" -c -g -Os -std=gnu11 -ffunction-sections -fdata-sections -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -MMD -MP -MF"UTFT/examples/Arduino (ARM) + Teensy/UTFT_Bitmap/tux.c.d" -MT"$@" -D__IN_ECLIPSE__=1 "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '


