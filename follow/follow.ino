#include <SoftwareSerial.h>

int i;                // Looping variable
int j;                // Looping variable
int inPin[3];         // Input pins coming from the ADC
int oldPin[3];
int roundPin[3];       // Rounded pin values
int outPin = 13;      // Output serial pin for motor control
int timeDelay = 100;    // Delay between issuing a signal and reading, milliseconds

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
int compare = 25;

int inVolt[2];  // Inputs to the Sabretooth

char buffer[100];

int lookup[][5] = {{0,0,0,0,0},{0,1,1,-7,7},{0,2,0,5,-5},{0,2,2,0,0},{0,4,1,-8,8},{0,4,2,-8,8},{1,0,1,9,7},{1,0,2,-4,6},{1,1,0,9,7},{2,0,3,-4,-9},{2,0,4,4,4},{2,3,0,0,0},{3,0,4,5,-5},{3,2,0,6,4},{3,4,0,9,7},{4,0,2,-6,5},{4,0,3,4,6},{4,2,0,-4,6}};
//int lookup[][5] = {{0,0,0, 0, 0},{0,0,1, 5,-5},{0,0,3, 5,-5},{0,0,3,5,-5},{0,0,4,5,-5}
//                  ,{0,1,0, 5,-5},{0,1,1, 5,-5},{0,1,2, 5,-5},{0,1,3,5,-5},{0,1,4,5,-5}
//                  ,{0,2,0, 6,-6},{0,2,1, 6,-6},{0,2,2, 6,-6},{0,2,3,7,-7},{0,2,4,8,-8}
//                  ,{0,3,0, 5,-5},{0,3,1, 5,-5},{0,3,2, 5,-5},{0,3,3,8,-8},{0,3,4,8,-8}
//                  ,{0,4,0,-8, 8},{0,4,1,-8, 8},{0,4,2,-7, 7},{0,4,3,6,-6},{0,4,4,6,-6}
//                  ,{1,0,0, 9, 7},{1,0,1, 9, 7},{1,0,2, 9, 7},{1,0,3,6, 4},{1,0,4,6, 2}
//                  ,{1,1,0, 9, 7},{1,1,1, 9, 7},{1,1,2, 9, 7},{1,1,3,6, 4},{1,1,4,6, 2}
//                  ,{1,2,0, 9, 7},{1,2,1, 9, 7},{1,2,2, 9, 7},{1,2,3,6, 4},{1,2,4,6, 2}
//                  ,{1,3,0, 9, 7},{1,3,1, 9, 7},{1,3,2, 9, 7},{1,3,3,6, 4},{1,3,4,6, 2}
//                  ,{1,4,0, 9, 7},{1,4,1, 9, 7},{1,4,2, 9, 7},{1,4,3,6, 4},{1,4,4,6, 2}
//                  ,{2,0,0, 6, 4},{2,0,1, 6, 4},{2,0,2, 6, 4},{2,0,3,6, 4},{2,0,4,6, 5}
//                  ,{2,3,0, 5, 6},{2,3,1, 5, 6},{2,3,2, 5, 6},{2,3,3,5, 6},{2,3,4,5, 6}
//                  ,{3,0,0, 9, 8},{3,0,1, 9, 8},{3,0,2, 9, 6},{3,0,3,9, 6},{3,0,4,9, 6}
//                  ,{3,1,0, 6, 8},{3,1,1, 6, 8},{3,2,2, 6, 8},{3,3,3,6, 9},{3,4,4,6, 9}
//                  ,{4,2,0, 8, 8},{4,2,1, 8, 8},{4,2,2, 8, 9},{4,2,3,9, 6},{4,2,4,9, 6}
//                  ,{4,3,0, 8, 8},{4,3,1, 8, 8},{4,3,2, 8, 9},{4,3,3,6, 9},{4,3,4,6, 9}};
//int lookup[][5] = {{}};


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

    // Find which values are the largest  
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
  
    // Initialize to random voltages
    inVolt[0] = random(-9,9);
    inVolt[1] = random(-9,9);
    
    if (inVolt[0] > 0 && inVolt[0] < 4)
    {
      inVolt[0] = 4;
    }
    else if (inVolt[0] <= 0 && inVolt[0] > -4)
    {
      inVolt[0] = -4;
    }
    if (inVolt[1] > 0 && inVolt[1] < 4)
    {
      inVolt[1] = 4;
    }
    else if (inVolt[1] <= 0 && inVolt[1] > -4)
    {
      inVolt[1] = -4;
    }
    
    sprintf(buffer, "inVolt[0]: %d\ninVolt[1]: %d\n", inVolt[0], inVolt[1]);
    Serial.print(buffer);
        
    // Look up situation, random values if not found
    for (i=0;i<sizeof(lookup)/sizeof(lookup[0]);i++)
    {      
      if (discrete[0] == lookup[i][0] && discrete[1] == lookup[i][1] && discrete[2] == lookup[i][2])
      {
        Serial.print("FOUND\n");
        Serial.print(i);
        inVolt[0] = lookup[i][3];
        inVolt[1] = lookup[i][4];
        break;
      }
    }

    sprintf(buffer, "System Input: %d %d %d\n", discrete[0], discrete[1], discrete[2]);
    Serial.print(buffer);
    sprintf(buffer, "System Output: %d %d\n", inVolt[0], inVolt[1]);
    Serial.print(buffer);
  
    // Assert the new voltages
    ST.write(byte(64 + inVolt[0] * 4));
    ST.write(byte(192 + inVolt[1] * 4));
    
    // Let the robot do its thing for a short amount of time
    delay(timeDelay);

    // Update the sensor values
    for (i=0;i<3;i++)
    {
      oldPin[i] = inPin[i];
      inPin[i] = analogRead(i);
    }
    
    // The packet to be stored
    sprintf(buffer, "Packet: %d,%d,%d,%d,%d,%d,%d,%d\n", oldPin[0], oldPin[1], oldPin[2], inVolt[0], inVolt[1], inPin[0], inPin[1], inPin[2]);
    Serial.print(buffer);
    
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
