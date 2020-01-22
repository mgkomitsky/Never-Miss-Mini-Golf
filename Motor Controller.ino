#include <Stepper.h>


// Example 4 - Receive a number as text and convert it to an int

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;

int projected_target_pixels = 0;            
int current_position = 0;
int pixels_per_step = 1;
int number_of_pixels = 0;
int number_of_steps = 0;



void setup() {

   
    
    Serial.begin(9600);  
    delay(1000);
    Serial.println("<Arduino is ready>");
    pinMode(LED_BUILTIN,OUTPUT);
    
    //homeDevice();
}





void loop() {
    recvWithEndMarker();
    showNewNumber();
}





void homeDevice()
{

    //Step left until switch triggers
    //Step to midpoint
    //Set current position to midpoint
  
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;
    
    if (Serial.available() > 0) {
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
        }
    }
}








void move_motor(int number_of_steps)
{


if(number_of_steps > 0)
  {

    //enable
    //set direction

      for (int i = 0; i <= number_of_steps; i++)

        {
          digitalWrite(7,HIGH);
          delay(10);
          digitalWrite(7,LOW);
        }
   
        //disable  
  } 

  else 
  
  {

    //enable
    //set direction
   

      for (int i = 0; i <= number_of_steps; i--)

        {
          digitalWrite(7,HIGH);
          delay(10);
          digitalWrite(7,LOW);
        }
      
        //disable  
  } 
  
  
}






int get_number_of_steps(int projected_target_pixels)
{
  number_of_pixels = projected_target_pixels - current_position;  
  number_of_steps = number_of_pixels * pixels_per_step;
  

  return number_of_steps;
  
}



void showNewNumber() {
    if (newData == true) 
    {
        projected_target_pixels = 0;             // new for this version
        projected_target_pixels = atoi(receivedChars);   // new for this version
        if (abs(projected_target_pixels)>100)
        {
         projected_target_pixels = 0; 
         }
      
        int steps = get_number_of_steps(projected_target_pixels);
        //Serial.print(steps);
        //Serial.print('\n');
        //Serial.print(projected_target_pixels);
        //Serial.print('\n');
        Serial.print(projected_target_pixels);
        Serial.print('\n');

        if(projected_target_pixels != current_position)
        {
        current_position = projected_target_pixels;
        move_motor(steps);
        }
        
        
        newData = false;
    }
}
