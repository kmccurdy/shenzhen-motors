/*
 * Reads target number of steps (= direction) from serial port.
 * Degree-to-step translation is handled in Python by the client. TODO: handle flip at 360 degrees
 */

#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *myMotor = AFMS.getStepper(200, 2);


int step_counter = 0;  // variable to count how many steps have been turned
int target = 0;   // variable to hold target step count data from serial  
String targetChar; // variable to hold target as string
int inChar;

void setup()
{
  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  myMotor->setSpeed(10);  // 10 rpm   
  Serial.begin(9600);    // open serial port
  Serial.print("Program Initiated\n");  
}


void loop()
{
    // While data is sent over serial assign it to the msg  
    while (Serial.available()>0){   
        // read new target
        inChar = Serial.read();
        if (isDigit(inChar)) {
          targetChar += (char)inChar;
        }
        if (inChar == '\n') {
          target = targetChar.toInt();
          Serial.print("Receiving Data:\n"); 
          Serial.println(target); 
        }
    }  

  // step until step counter matches target
  if (target == 2000) {
      Serial.write(step_counter); // interpret 2000 as querying counter state
  } else if (target > step_counter) {
      while (target > step_counter){
        myMotor->step(1, FORWARD, SINGLE);  
        ++step_counter;   
      }   
      targetChar = "";
      // print current status
      Serial.println("Step Counter:");
      Serial.println(step_counter); 
      Serial.println("Target:");
      Serial.println(target); 
  } else if (target < step_counter) {
      while (target < step_counter){
        myMotor->step(1, BACKWARD, SINGLE);  
        --step_counter;
      }   
      targetChar = "";
      // print current status
      Serial.println("Step Counter:");
      Serial.println(step_counter); 
      Serial.println("Target:");
      Serial.println(target); 
  } 
}
