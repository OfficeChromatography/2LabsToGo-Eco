/**
 * 
 * 2LabsToGo Humidity Control
 * Copyright (c) 2024 Food Science JLU
 *  
 * Marlin 3D Printer Firmware
 * Copyright (c) 2020 MarlinFirmware [https://github.com/MarlinFirmware/Marlin]
 *
 * Based on Sprinter and grbl.
 * Copyright (c) 2011 Camiel Gubbels / Erik van der Zalm
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#include "../gcode.h"
#include "../../MarlinCore.h"  //for pin_is_protected
#include "../../inc/MarlinConfig.h"
#include "DHT.h"


extern DHT dht;
unsigned long hum_check_interval_up = 10000;
float humidity_up;



void check_humidity_and_toggle_fan_up() {

   #define FAN_PIN 9 
   pinMode(FAN_PIN, OUTPUT);

   for (int i = 1; i <= 2; i++){
      humidity_up = dht.readHumidity(true);
      delay(200);
   }

   humidity_up = dht.readHumidity(true);

   if (isnan(humidity_up)) {
         SERIAL_ECHO_START();
         SERIAL_ECHOLN("Failed to read from DHT sensor!");
         return;
   }

   if (humidity_up <= threshold) {
      digitalWrite(FAN_PIN, HIGH);  // Turn the fan on
   } else {
      digitalWrite(FAN_PIN, LOW);  // Turn the fan off
   }
 
   SERIAL_ECHOLNPAIR("Humidity: ", humidity_up, "%");
   delay(500);
   SERIAL_ECHOLNPAIR("Fan State: ", humidity_up <= threshold ? "ON" : "OFF");
   delay(500);
}

void check_deviation_up(){
 
   float deviation_up = abs(humidity_up - threshold);

   if (deviation_up >= 20){
      hum_check_interval_up = 20000;
      //analogWrite(FAN_PIN, 255);  //fan full speed
   }else if(deviation_up < 20 && deviation_up >= 5){
      hum_check_interval_up = 5000;
      //analogWrite(FAN_PIN, 200);  //fan S200
   }else if(deviation_up < 5 && deviation_up >= 2){
      hum_check_interval_up = 2000;   
      //analogWrite(FAN_PIN, 150);  //fan S150
   }else{
      hum_check_interval_up = 1000;  //deviation < 2
      //analogWrite(FAN_PIN, 100);  //fan S100
   } 
}

void periodic_humidity_check_up() {
    // Only check the humidity at the specified interval
    static unsigned long lasthumidityCheck = 0;
    
    if (millis() - lasthumidityCheck > hum_check_interval_up) {
        lasthumidityCheck = millis();
        check_humidity_and_toggle_fan_up();  // Perform the check and control the fan
        check_deviation_up();
    }
  
}

void GcodeSuite::M1200()
{  
   #define FAN_PIN 9 
   pinMode(FAN_PIN, OUTPUT);
   if (parser.seenval('A')){
      if (parser.value_int() == 1){
         is_dryingH_active_up = true;
         SERIAL_ECHOLNPGM("Humidity sensor is enabled!");
         delay(500);
      }
      else if(parser.value_int() == 0){
         is_dryingH_active_up = false;
         digitalWrite(FAN_PIN, LOW);  // Turn the fan off
         delay(500);
         SERIAL_ECHOLNPGM("Humidity sensor is disabled!");
      }
   }


   if (parser.seenval('T')) {
     
      threshold = parser.value_int();
      SERIAL_ECHOLNPAIR("Humidifying threshold was set to: ", threshold);
      
      
      
   }


}
