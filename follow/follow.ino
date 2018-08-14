#include <SoftwareSerial.h>

int i;                // Looping variable
int j;                // Looping variable
int inPin[3];         // Input pins coming from the ADC
int roundPin[3];       // Rounded pin values
int outPin = 13;      // Output serial pin for motor control
int timeDelay = 500;    // Delay between issuing a signal and reading, milliseconds

int proxPin = 11;     // Digital input pin used for the proximity sensor
int proxVal;          // Value from the input of the proximity pin

int range;
int high;
int mid;
int index[3];
int indexAlt[3];
int normal[3];
int discrete[3];
int mode[3];          // Contains the mode values obtained from calibration
int motorSpeed = 17;  // The general speed of the robot
int compare = 50;

int inputVoltage[2];  // Inputs to the Sabretooth

//int lookup[][5] = {{0,0,0,0,0},{0,0,1,-3,1},{0,0,3,-5,1},{0,1,1,-2,-4},{0,2,2,4,2},{0,2,3,-9,2},{0,2,4,0,1},{0,3,2,0,4},{0,3,4,-5,-4},{0,4,1,-8,2},{0,4,2,-4,2},{0,4,3,0,-7},{1,0,1,-9,-7},{1,0,4,2,2},{2,0,4,-6,-9},{2,3,0,2,2},{3,0,4,-8,8},{3,4,0,3,3},{4,1,0,-7,-7},{4,2,0,-9,-8},{4,3,0,2,4}};
int lookup[][5] = {{0,0,0,0,0},{0,0,1,5,-5},{0,0,3,5,-5},{0,1,1,5,-5},{0,2,2,6,-6},{0,2,3,7,-7},{0,2,4,8,-8},{0,3,2,5,-5},{0,3,4,8,-8},{0,4,1,-8,8},{0,4,2,-7,7},{0,4,3,6,-6},{1,0,1,9,7},{1,0,3,6,4},{1,0,4,6,2},{2,0,2,6,4},{2,0,4,6,5},{2,3,0,5,6},{3,0,1,9,8},{3,0,4,9,6},{3,2,0,6,8},{3,4,0,6,9},{4,0,1,8,8},{4,0,2,8,9},{4,0,3,9,6},{4,1,0,8,8},{4,2,0,8,9},{4,3,0,6,9}};


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
    for (i = 0; i < 3; i++)
    {
      inPin[i] = analogRead(i);
//      Serial.print(inPin[i]);
//      Serial.print(",");
//      Serial.print(mode[i]);
//      if (i != 2)
//      {
//        Serial.print(",");
//      }
    }
    Serial.print("\n");
  
  
  
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
    
    for (i=0;i<3;i++)
    {
      // Reset index
      index[i] = 0;
      
      for (j=0;j<3;j++)
      {
        if (i != j && inPin[i] > inPin[j])
        {
          index[i]++;
        }
      }
    }
    
    for (i=0;i<3;i++)
    {
      if (index[i] == 0)
      {
        indexAlt[2] = i;
      }
      else if (index[i] == 1)
      {
        indexAlt[1] = i;
      }
      else if (index[i] == 2)
      {
        indexAlt[0] = i;
      }
    }
       
    // Prepare values for the lookup table
    for (i=0;i<3;i++)
    {
      normal[i] = inPin[i] - mode[i];
    }
   
    range = normal[indexAlt[0]] - normal[indexAlt[1]];
    
    if (range >= 9*compare)
    {
      high = 4;
    }
    else if (range >= 7*compare)
    {
      high = 3; 
    }
    else if (range >= 5*compare)
    {
      high = 2; 
    }
    else if (range >= 2*compare)
    {
      high = 1; 
    }
    else
    {
      high = 0; 
    }
    
    
    if (normal[indexAlt[1]] >= range/4)
    {
      mid = round(high/4);
    }
    else if (normal[indexAlt[1]] >= 2*range/4)
    {
      mid = round(2*high/4);
    }  
    else if (normal[indexAlt[1]] >= 3*range/4)
    {
      mid = round(3*high/4);
    }
    else if (normal[indexAlt[1]] == normal[indexAlt[0]])
    {
      mid = high;
    }
    else if (normal[indexAlt[1]] >= normal[indexAlt[2]])
    {
      mid = 0;
    }  
    
    discrete[indexAlt[0]] = high;
    discrete[indexAlt[1]] = mid;
    discrete[indexAlt[2]] = 0;
    
    // Look up situation, random values if not found
    for (i=0;i<sizeof(lookup);i++)
    {      
      if (discrete[0] == lookup[i][0] && discrete[1] == lookup[i][1] && discrete[2] == lookup[i][2])
      {
        Serial.print("FOUND\n");
        inputVoltage[0] = lookup[i][3];
        inputVoltage[1] = lookup[i][4];
        break;
      }
    }
    
    Serial.print("System Input: ");
    Serial.print(discrete[0]);
    Serial.print(discrete[1]);
    Serial.print(discrete[2]);
    Serial.print("\n");
    Serial.print("System Output: ");
    Serial.print(inputVoltage[0]);
    Serial.print(inputVoltage[1]);
    Serial.print("\n");
  
    // Assert the new voltages
    ST.write(byte(64 + inputVoltage[0] * 5));
    ST.write(byte(192 + inputVoltage[1] * 5));
    
    delay(timeDelay);

//    Serial.print("Packet: ");
//    // Print the input sensor data to be used for the test
//    for (i=0;i<3;i++)
//    {
//      Serial.print(inPin[i]);
//      Serial.print(",");
//      inPin[i] = analogRead(i);
//    }
//    
//    // Print the voltages that will be used for the test
//    Serial.print(inputVoltage[0]);
//    Serial.print(",");
//    Serial.print(inputVoltage[1]);
//    Serial.print(",");
//    
//    // Print the output sensor values of the test
//    Serial.print(inPin[0]);
//    Serial.print(",");
//    Serial.print(inPin[1]);
//    Serial.print(",");
//    Serial.print(inPin[2]);
//    Serial.print("\n");
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
