//#include <NewSoftSerial.h>
#include <SoftwareSerial.h>
//#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

//NewSoftSerial mySerial(4, 2); // RX, TX

SoftwareSerial mySerial(4, 2); // RX, TX
int ledpin=13; // led on D13 will show blink on / off
int BluetoothData; // the data given from Computer

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);
// you can also call it with a different address and I2C interface
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40, &Wire);

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define SERVOMIN  400 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  750 // this is the 'maximum' pulse length count (out of 4096)

// our servo # counter
uint8_t servonum = 0;
// Here we store previous finger's number
uint8_t previous_finger_servo_number = 50;

void open_all_fingers()
{
  // INITIALLY WE BEGIN BY CLOSING ALL FINGERS ONE BY ONE
  for (int i=0;i<5;i++)
  {
    for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen--) 
    {
      pwm.setPWM(i, 0, pulselen);
    }

    // Stop all motors after they are closed so they dont vibrate.
    pwm.setPWM(i, 0, 4096);

    delay(500);
  }
}

void close_all_fingers()
{
  // INITIALLY WE BEGIN BY CLOSING ALL FINGERS ONE BY ONE
  for (int i=0;i<5;i++)
  {
    for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen++) 
    {
      pwm.setPWM(i, 0, pulselen);
    }

    // Stop all motors after they are closed so they dont vibrate.
    pwm.setPWM(i, 0, 4096);

    delay(500);
  }
}

void setup() 
{
  // put your setup code here, to run once:
  mySerial.begin(9600);
  pinMode(ledpin,OUTPUT);
  
  pwm.begin();
  
  
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
  // First open all fingers .. wait for 5 seconds 
//  open_all_fingers();
//  delay(2000);
  //delay(10);
  // Then close all fingers
  close_all_fingers();
}

// you can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
void setServoPulse(uint8_t n, double pulse) 
{
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 60;   // 60 Hz
//  Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
//  Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000000;  // convert to us
  pulse /= pulselength;
//  Serial.println(pulse);
  pwm.setPWM(n, 0, pulse);
}

void finger_open(uint8_t servonum)
{

  // Open the classified finger
  for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen--) 
  {
    pwm.setPWM(servonum, 0, pulselen);
  }
  // This line stops the motor so that it doesnt keep "buzzing"
  pwm.setPWM(servonum,0,4096);      
  delay(200);
  
}

void finger_close(uint8_t servonum)
{
  // Close the previous finger
  
  for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen++) 
  {
    pwm.setPWM(servonum, 0, pulselen);
  }
  
  // This line stops the motor so that it doesnt keep "buzzing"
  pwm.setPWM(servonum,0,4096);      
  delay(200);

}

void loop() 
{
  if (mySerial.available()>0) 
  {    
    // We read the bluetooth data. In this case the finger to be moved by servo motor
    BluetoothData=mySerial.read();
    if (BluetoothData == '0')
    {
      servonum = 0;
    }
    else if (BluetoothData == '1')
    {
      servonum = 1;
    }
    else if (BluetoothData == '2')
    {
      servonum = 2;
    }
    else if (BluetoothData == '3')
    {
      servonum = 3;
    }
    else if (BluetoothData == '4')
    {
      servonum = 4;
    }
    else if (BluetoothData == '5')
    {
      servonum = 5;
    }
    else if (BluetoothData == '6')
    {
      servonum = 6;
    }
    else if (BluetoothData == '7')
    {
      servonum = 7;
    }
    else if (BluetoothData == '8')
    {
      servonum = 8;
    }
    else if (BluetoothData == '9')
    {
      servonum = 9;
    }
    else if (BluetoothData == 'a')
    {
      servonum = 10;
    }
    else if (BluetoothData == 'b')
    {
      servonum = 11;
    }
    else
    {
    
    }
    mySerial.write(BluetoothData);
    digitalWrite(ledpin,!digitalRead(ledpin));
    // If previous finger was different than the received finger servo number then open received servo number
    if (previous_finger_servo_number != servonum)
    {
      // If fingers are between thumb and pinky, then open the received finger and close the previous open finger
      if (servonum==0)
      {        
        finger_open(0);
        finger_close(1);
        finger_close(2);
        finger_close(3);
        finger_close(4);        
      }

      else if (servonum==1)
      {        
        finger_open(1);
        finger_close(0);
        finger_close(2);
        finger_close(3);
        finger_close(4);        
      }

      else if (servonum==2)
      {        
        finger_open(2);
        finger_close(0);
        finger_close(1);
        finger_close(3);
        finger_close(4);
        
      }

      else if (servonum==3)
      {        
        finger_open(3);        
        finger_close(0);
        finger_close(1);
        finger_close(2);
        finger_close(4);        
      }

      else if (servonum==4)
      {        
        finger_open(4);        
        finger_close(0);
        finger_close(1);
        finger_close(2);
        finger_close(3);        
      }
     
      // Two fingers open i.e. index and middle
      else if (servonum == 5)
      {
        finger_close(0);
        finger_close(3);
        finger_close(4);
        finger_open(1);
        finger_open(2);
      }

      // Three fingers open i.e. index, middle and ring
      else if (servonum == 6)
      {
        finger_close(0);
        finger_close(4);
        finger_open(1);
        finger_open(2);
        finger_open(3);
      }

      // Four fingers open i.e. index, middle, ring and pinky
      else if (servonum == 7)
      {
        finger_close(0);
        finger_open(1);
        finger_open(2);
        finger_open(3);
        finger_open(4);          
      }

      // Five fingers open i.e. index, middle and ring
      else if (servonum == 8)
      {
        finger_open(0);
        finger_open(1);
        finger_open(2);
        finger_open(3);
        finger_open(4);          
      }

      // All fingers closed (fist)
      else if (servonum == 9 || servonum == 10)
      {
        finger_close(0);
        finger_close(1);
        finger_close(2);
        finger_close(3);
        finger_close(4);          
      }

        // Pick movement. Thumb, index middle close rest open
      else if (servonum == 11)
      {
        finger_close(0);
        finger_close(1);
        finger_close(2);
        finger_open(3);
        finger_open(4);          
      }
      
      previous_finger_servo_number = servonum;

    }
    delay(100);
  }
}
