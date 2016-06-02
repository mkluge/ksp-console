################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
PDE_SRCS += \
C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/chipKit/UTFT_Bitmap_128x128/UTFT_Bitmap_128x128.pde 

C_SRCS += \
C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/chipKit/UTFT_Bitmap_128x128/icon1.c \
C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/chipKit/UTFT_Bitmap_128x128/icon2.c \
C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/chipKit/UTFT_Bitmap_128x128/tux.c 

PDE_DEPS += \
./UTFT/examples/chipKit/UTFT_Bitmap_128x128/UTFT_Bitmap_128x128.pde.d 

C_DEPS += \
./UTFT/examples/chipKit/UTFT_Bitmap_128x128/icon1.c.d \
./UTFT/examples/chipKit/UTFT_Bitmap_128x128/icon2.c.d \
./UTFT/examples/chipKit/UTFT_Bitmap_128x128/tux.c.d 

LINK_OBJ += \
./UTFT/examples/chipKit/UTFT_Bitmap_128x128/icon1.c.o \
./UTFT/examples/chipKit/UTFT_Bitmap_128x128/icon2.c.o \
./UTFT/examples/chipKit/UTFT_Bitmap_128x128/tux.c.o 


# Each subdirectory must supply rules for building sources it contributes
UTFT/examples/chipKit/UTFT_Bitmap_128x128/UTFT_Bitmap_128x128.o: C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/chipKit/UTFT_Bitmap_128x128/UTFT_Bitmap_128x128.pde
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '

UTFT/examples/chipKit/UTFT_Bitmap_128x128/icon1.c.o: C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/chipKit/UTFT_Bitmap_128x128/icon1.c
	@echo 'Building file: $<'
	@echo 'Starting C compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-gcc" -c -g -Os -std=gnu11 -ffunction-sections -fdata-sections -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '

UTFT/examples/chipKit/UTFT_Bitmap_128x128/icon2.c.o: C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/chipKit/UTFT_Bitmap_128x128/icon2.c
	@echo 'Building file: $<'
	@echo 'Starting C compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-gcc" -c -g -Os -std=gnu11 -ffunction-sections -fdata-sections -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '

UTFT/examples/chipKit/UTFT_Bitmap_128x128/tux.c.o: C:/Users/mkluge/Documents/Arduino/libraries/UTFT/examples/chipKit/UTFT_Bitmap_128x128/tux.c
	@echo 'Building file: $<'
	@echo 'Starting C compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-gcc" -c -g -Os -std=gnu11 -ffunction-sections -fdata-sections -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '


