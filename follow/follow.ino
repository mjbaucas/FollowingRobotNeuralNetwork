#include <SoftwareSerial.h>

int i;                // Looping variable
int j;                // Looping variable
int inPin[3];         // Input pins coming from the ADC
int roundPin[3];       // Rounded pin values
int outPin = 13;      // Output serial pin for motor control
int timeDelay = 100;    // Delay between issuing a signal and reading, milliseconds

int proxPin = 11;     // Digital input pin used for the proximity sensor
int proxVal;          // Value from the input of the proximity pin

int mode[3];          // Contains the mode values obtained from calibration
int motorSpeed = 17;  // The general speed of the robot

int inputVoltage[2];  // Inputs to the Sabretooth

unsigned long startTime = 0;  // Used for measuring time
unsigned long totalTime = 0;  // Used for measuring time

int lookup[][5] = {{100, 200, 300, 2, 3}
                 ,{500, 600, 600, 4, -5}
                 ,{50 , 50 , 50 , 1, 1}};

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
//    // Get the new values of each analog input and print it to the serial monitor
//    for (i = 0; i < 3; i++)
//    {
//      inPin[i] = analogRead(i);
//      Serial.print(inPin[i]);
//      Serial.print(",");
//      Serial.print(mode[i]);
//      if (i != 2)
//      {
//        Serial.print(",");
//      }
//    }
//    Serial.print("\n");
  
    // Use the neural network to find the input voltages
    // Round the sensor values
    for (i=0;i<3;i++)
    {
      roundPin[i] = roundTo(inPin[i], 50);
    }
//    Serial.print("Rounded: ");
//    for (i=0;i<3;i++)
//    {
//      Serial.print(roundPin[i]);
//      Serial.print(",");
//    }
//    Serial.print("\n");
    
    // Initialize to random voltages
    inputVoltage[0] = random(-9,9);
    inputVoltage[1] = random(-9,9);
    
    // Look up situation, random values if not found
    for (i=0;i<sizeof(lookup);i++)
    {
      if (roundPin[0] == lookup[i][0] && roundPin[1] == lookup[i][1] && roundPin[2] == lookup[i][2])
      {
        inputVoltage[0] = lookup[i][3];
        inputVoltage[1] = lookup[i][4];
      }
    }
  
    // Assert the new voltages
    ST.write(byte(64 + inputVoltage[0] * 5));
    ST.write(byte(192 + inputVoltage[1] * 5));
    
    delay(timeDelay);

    // Print the input sensor data to be used for the test
    for (i=0;i<3;i++)
    {
      Serial.print(inPin[i]);
      Serial.print(",");
      inPin[i] = analogRead(i);
    }
    
    // Print the voltages that will be used for the test
    Serial.print(inputVoltage[0]);
    Serial.print(",");
    Serial.print(inputVoltage[1]);
    Serial.print(",");
    
    // Print the output sensor values of the test
    Serial.print(inPin[0]);
    Serial.print(",");
    Serial.print(inPin[1]);
    Serial.print(",");
    Serial.print(inPin[2]);
    Serial.print("\n");
  }
}

int roundTo(int number, int multiple)
{
  int i;
  int tmpNum = number;
  
  while(tmpNum - multiple > 0)
  {
    tmpNum -= multiple;
  }
  
  if(tmpNum > multiple / 2)
  {
    // Round up
    number = number - tmpNum + multiple;
  }
  else
  {
    // Round down
    number = number - tmpNum;
  }
  return number;
}
