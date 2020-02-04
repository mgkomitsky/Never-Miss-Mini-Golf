


// Example 4 - Receive a number as text and convert it to an int

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;

int projected_target_pixels = 0;            
int current_position_pixels = 50;
int pixels_per_step = 2;
int number_of_pixels = 0;
int number_of_steps = 0;
int target_zone_length_in_steps = 10;
int small_boundary = 0;
int big_boundary = 3000;


int left_limit_switch = 2;
int right_limit_switch = 3;
int direction_pin = 9;
int enable_pin = 10;
int motor_pulse_pin = 7;


void setup() {

   
    
    Serial.begin(9600);  
    delay(1000);
    //Serial.println("<Arduino is ready>");
    pinMode(LED_BUILTIN,OUTPUT);
    pinMode(9,OUTPUT); //Direction
    pinMode(10, OUTPUT); //Enable
    pinMode(7, OUTPUT); //Pulse
    //pinMode(2,INPUT); //Right Limit
    //pinMode(3,INPUT); //Left Limit
    //attachInterrupt(digitalPinToInterrupt(left_limit_switch), homeDevice_towards_right, CHANGE);
    //attachInterrupt(digitalPinToInterrupt(right_limit_switch), homeDevice_towards_left, CHANGE);

    //digitalWrite(motor_pulse_pin,LOW);
    
    
    //homeDevice_towards_left();
}





void loop() {
  
  
    recvWithEndMarker();
    showNewNumber();
}



void homeDevice_towards_right()
{

    while(digitalRead(left_limit_switch)==LOW)
    {
      move_motor(1);
    }

 
     
     move_motor(round(-target_zone_length_in_steps/2)); //Must be an integer
     current_position_pixels == target_zone_length_in_steps/2;
  
}

void homeDevice_towards_left()
{

    while(digitalRead(right_limit_switch)==LOW)
    {
      move_motor(-1);
    }

     
     move_motor(round(target_zone_length_in_steps/2)); //Must be an integer
     current_position_pixels == target_zone_length_in_steps/2;
  
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

        digitalWrite(enable_pin,LOW);//enable
        digitalWrite(direction_pin,HIGH);//set direction

      for (int i = 0; i <= number_of_steps; i++)

        {
          digitalWrite(motor_pulse_pin,HIGH);
          delay(1);
          digitalWrite(motor_pulse_pin,LOW);
          
        }
   
        digitalWrite(enable_pin,HIGH);//disable  
  } 

  else 
  
  {
        digitalWrite(10,LOW);//enable
        digitalWrite(direction_pin,LOW);//set direction
   

      for (int i = 0; i >= number_of_steps; i--)

        {
          digitalWrite(motor_pulse_pin,HIGH);
          delay(1);
          digitalWrite(motor_pulse_pin,LOW);
         
        }
      
        digitalWrite(10,HIGH);//disable  
  } 
  
}






int get_number_of_steps(int projected_target_pixels)
{
  number_of_pixels = projected_target_pixels - current_position_pixels;  
  number_of_steps = number_of_pixels * pixels_per_step;
  

  return number_of_steps;
  
}



void showNewNumber() {
    if (newData == true) 
    {
        projected_target_pixels = 0;            
        projected_target_pixels = atoi(receivedChars);   
        if (abs(projected_target_pixels)>2000)
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

        if(projected_target_pixels != current_position_pixels && projected_target_pixels > small_boundary && projected_target_pixels < big_boundary)
        {
        current_position_pixels = projected_target_pixels;
        move_motor(steps);
        }
        
        
        newData = false;
    }
}
