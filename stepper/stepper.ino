/*
 * Reads target number of steps (= direction) from serial port.
 * Degree-to-step translation is handled in Python by the client. TODO: handle flip at 360 degrees
 */

#include <Stepper.h>

// number of steps on our motor
#define STEPS 200

// create an instance of the stepper class, specifying
// the number of steps of the motor and the pins it's
// attached to
Stepper stepper(STEPS, 8, 9, 10, 11);

int step_counter = 0;  // variable to count how many steps have been turned
int target = 0;   // variable to hold target step count data from serial  

void setup()
{
  stepper.setSpeed(30);  // set the speed of the motor to 30 RPMs
  Serial.begin(9600);    // open serial port
  Serial.print("Program Initiated\n");  
}

void loop()
{
    // While data is sent over serial assign it to the msg  
    while (Serial.available()>0){   
        target=Serial.read();  
        Serial.print("Receiving Data\n"); 
        Serial.print(target); 
        Serial.print("\n"); 
    }  

  // step until step counter matches target
  if (target == 2000) {
      Serial.write(step_counter); // interpret 2000 as querying counter state
  } else if (target > step_counter) {
      while (target > step_counter){
        stepper.step(1);  
        step_counter++;
      }   
  } else if (target < step_counter) {
      while (target < step_counter){
        stepper.step(-1);  
        step_counter--;
      }   
  }
  Serial.print("Step Counter:\n");
        Serial.print(step_counter); 
        Serial.print("\n"); 
}
