// custom Gcode 1200 test
#include "../gcode.h"
#include "../../MarlinCore.h"  //for pin_is_protected
#include "../../inc/MarlinConfig.h"
#include "DHT.h"

extern DHT dht;

void GcodeSuite::M1200() {
         // This is where you define the actions of the M1100 command.
         // Example: Print a message to the serial monitor.
    SERIAL_ECHO_START();
    SERIAL_ECHOLN("M1100 Command Executed");

         // Additional custom code can be added here, like controlling a pin:
    #define CUSTOM_PIN 9
    SET_OUTPUT(CUSTOM_PIN);
    WRITE(CUSTOM_PIN, HIGH); // Example: setting a pin to HIGH
    delay(5000);
    WRITE(CUSTOM_PIN, LOW); // Example: setting a pin to LOW 
}
