################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
INO_SRCS += \
C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/TI\ LaunchPads\ (Energia)/UTFT_Textrotation_Demo/UTFT_Textrotation_Demo.ino 

INO_DEPS += \
./UTFT/examples/TI\ LaunchPads\ (Energia)/UTFT_Textrotation_Demo/UTFT_Textrotation_Demo.ino.d 


# Each subdirectory must supply rules for building sources it contributes
UTFT/examples/TI\ LaunchPads\ (Energia)/UTFT_Textrotation_Demo/UTFT_Textrotation_Demo.o: C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/TI\ LaunchPads\ (Energia)/UTFT_Textrotation_Demo/UTFT_Textrotation_Demo.ino
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -MMD -MP -MF"UTFT/examples/TI LaunchPads (Energia)/UTFT_Textrotation_Demo/UTFT_Textrotation_Demo.ino.d" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '


