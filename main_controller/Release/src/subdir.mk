################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
C:/Users/mkluge/Documents/Arduino/libraries/ArduinoJson/src/JsonArray.cpp \
C:/Users/mkluge/Documents/Arduino/libraries/ArduinoJson/src/JsonBuffer.cpp \
C:/Users/mkluge/Documents/Arduino/libraries/ArduinoJson/src/JsonObject.cpp \
C:/Users/mkluge/Documents/Arduino/libraries/ArduinoJson/src/JsonVariant.cpp 

LINK_OBJ += \
./src/JsonArray.cpp.o \
./src/JsonBuffer.cpp.o \
./src/JsonObject.cpp.o \
./src/JsonVariant.cpp.o 

CPP_DEPS += \
./src/JsonArray.cpp.d \
./src/JsonBuffer.cpp.d \
./src/JsonObject.cpp.d \
./src/JsonVariant.cpp.d 


# Each subdirectory must supply rules for building sources it contributes
src/JsonArray.cpp.o: C:/Users/mkluge/Documents/Arduino/libraries/ArduinoJson/src/JsonArray.cpp
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\cores\arduino" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\variants\mega" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire\src" -I"C:\Users\mkluge\Documents\Arduino\libraries\ArduinoJson\src" -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '

src/JsonBuffer.cpp.o: C:/Users/mkluge/Documents/Arduino/libraries/ArduinoJson/src/JsonBuffer.cpp
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\cores\arduino" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\variants\mega" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire\src" -I"C:\Users\mkluge\Documents\Arduino\libraries\ArduinoJson\src" -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '

src/JsonObject.cpp.o: C:/Users/mkluge/Documents/Arduino/libraries/ArduinoJson/src/JsonObject.cpp
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\cores\arduino" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\variants\mega" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire\src" -I"C:\Users\mkluge\Documents\Arduino\libraries\ArduinoJson\src" -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '

src/JsonVariant.cpp.o: C:/Users/mkluge/Documents/Arduino/libraries/ArduinoJson/src/JsonVariant.cpp
	@echo 'Building file: $<'
	@echo 'Starting C++ compile'
	"C:\Program Files\eclipseArduino\arduinoPlugin\tools\arduino\avr-gcc\4.8.1-arduino5/bin/avr-g++" -c -g -Os -std=gnu++11 -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -MMD -mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO=10606 -DARDUINO_AVR_MEGA2560 -DARDUINO_ARCH_AVR     -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\cores\arduino" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\variants\mega" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire" -I"C:\Program Files\eclipseArduino\arduinoPlugin\packages\arduino\hardware\avr\1.6.11\libraries\Wire\src" -I"C:\Users\mkluge\Documents\Arduino\libraries\ArduinoJson\src" -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -D__IN_ECLIPSE__=1 -x c++ "$<"  -o  "$@"   -Wall
	@echo 'Finished building: $<'
	@echo ' '


