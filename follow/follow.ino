#include <SoftwareSerial.h>

int i;                // Looping variable
int j;                // Looping variable
int inPin[3];         // Input pins going to the ADC
int outPin = 13;      // Output serial pin for motor control
int timeDelay = 20;    // Delay between issuing a signal and reading, milliseconds
int threshold = 50;   // Value needed to be surpassed for robot to react

int proxPin = 11;     // Digital input pin used for the proximity sensor
int proxVal;          // Value from the input of the proximity pin

int mode[3];          // Contains the mode values obtained from calibration
int motorSpeed = 17;  // The general speed of the robot

int inputVoltage[2];  // Inputs to the Sabretooth

int timeout = 3000;   // Timeout in milliseconds of waiting for the front sensor to be reached

unsigned long startTime = 0;  // Used for measuring time
unsigned long totalTime = 0;  // Used for measuring time

char* packet = "";            // String to be sent to the Pi during transmission

SoftwareSerial ST = SoftwareSerial(0, 13); // Serial variable to control the motor

void setup() {
  Serial.begin(9600);
  pinMode(outPin, OUTPUT);

  inPin[0] = 0;
  inPin[1] = 0;
  inPin[2] = 0;

  ST = SoftwareSerial(0, outPin);
  ST.begin(9600);

  // Calibration
  for(i=0;i<3;i++)
  {
    j = 0;
    while(j < 5)
    {
      mode[i] = analogRead(i);
      if (mode[i] < analogRead(i) - 50 && mode[i] > analogRead(i) + 50)
      {
        mode[i] = analogRead(i);
        j = 0;
      }
      delay(10);
      j++;
    }
    Serial.print("\nMode: ");
    Serial.print(i);
    Serial.print(": ");
    Serial.print(mode[i]);
    Serial.print("\n");
  }
}

void loop() {
  // Read the digital value of the proimity sensor
  proxVal = digitalRead(proxPin);

  // Stop the robot if the proximity detector is triggered
  if (proxVal > 0)
  {
    // Get the new values of each analog input and print it to the serial monitor
    for (i = 0; i < 3; i++)
    {
      inPin[i] = analogRead(i);
      Serial.print(inPin[i]);
      Serial.print(",");
      Serial.print(mode[i]);
      if (i != 2)
      {
        Serial.print(",");
      }
    }
    Serial.print("\n");

//    // If the front reciever can see it
//    if (inPin[0] > mode[0] + threshold
//     && inPin[0] - mode[0] > inPin[1] - mode[1]
//     && inPin[0] - mode[0] > inPin[2] - mode[2])
//    {
//      goStraight();
//    }
//
//    // If the right side recievers can see it
//    else if (inPin[1] > mode[1] + threshold
//          && inPin[1] - mode[1] > inPin[0] - mode[0]
//          && inPin[1] - mode[1] > inPin[2] - mode[2])
//    {
//      goClock();
//    }
//
//    // If the left side recievers can see it
//    else if (inPin[2] > mode[2] + threshold
//          && inPin[2] - mode[2] > inPin[0] - mode[0]
//          && inPin[2] - mode[2] > inPin[1] - mode[1])
//    {
//      goCounterClock();
//    }
//    else
//    {
//      goStop();
//    }

    // Use the neural network to find the input voltages
    inputVoltage[0] = random(-9,9);
    inputVoltage[1] = random(-9,9);

    // Assert the new voltages
    ST.write(byte(64 + inputVoltage[0] * 7));
    ST.write(byte(192 + inputVoltage[1] * 7));
    delay(timeDelay);

    // Report all the data associated with this cycle if the front sensor was spiked
    // Start a timer
    startTime = millis();

    // Wait until the front sensor threshold is passed or the timeout is reached
    while (inPin[0] < mode[0] + threshold + 500 && millis() - startTime < timeout)
    {
      inPin[0] = analogRead(0);
      delay(timeDelay);
      //Serial.print("Waiting\n");
    }

    if (inPin[0] >= mode[0] + threshold || 1)
    {
      totalTime = millis() - startTime;
  
      // Format serial packet
      //packet = inPin[0] + "," + inPin[1] + "," + inPin[2] + "," + inputVoltage[0] + ","+inputVoltage[1] + "," + totalTime;
      //packet = inPin[0] + "," + inPin[1];
      Serial.print("Packet: ");
      Serial.print(inPin[0]);
      Serial.print(",");
      Serial.print(inPin[1]);
      Serial.print(",");
      Serial.print(inPin[2]);
      Serial.print(",");
      Serial.print(inputVoltage[0]);
      Serial.print(",");
      Serial.print(inputVoltage[1]);
      Serial.print(",");
      Serial.print(totalTime);
      Serial.print("\n");
      delay(50);
      
      // Send the packet
      //Serial.println(packet);
    }
  }
//  else
//  {
//    goStop();
//  }
}

//// Stop
//void goStop()
//{
//  ST.write(byte(64));
//  ST.write(byte(192));
//  delay(timeDelay);
//}
//
//// Go forward
//void goStraight()
//{
//  ST.write(byte(64 + motorSpeed));
//  ST.write(byte(192 + motorSpeed));
//  delay(timeDelay);
//}
//
//// Turn clockwise
//void goClock()
//{
//  ST.write(byte(64 + motorSpeed));
//  ST.write(byte(192 - motorSpeed));
//  delay(timeDelay);
//}
//
//// Turn counterclockwise
//void goCounterClock()
//{
//  ST.write(byte(64 - motorSpeed));
//  ST.write(byte(192 + motorSpeed));
//  delay(timeDelay);
//}
 
