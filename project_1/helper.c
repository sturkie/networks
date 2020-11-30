#include "RIMS.h"

//Notes:

//Target speed is 100

//Inputs
//A0 = PID Control / Manual Control
//A1 = Output Mode Control ( Numerical or Visual representation)
//IF A0, A6 = Fan Speed Up, A7 = Fan Speed Down, A6 & A7 = Nothing

//Outputs
//B = Ball's Height (target 100)

//Equation: Actuator = Kp*Error + Ki*Integ - Kd*Deriv

int CONST_P = 50;
int CONST_I = 1;
int CONST_D = 2500;

int desired = 100;
int actual = 0;

unsigned char fan_speed = 0;

int actuator = 0;
int error = 0;
int integral = 0;
int deriv = 0;
int actual_prev = 0;

int g = 9800;
int dt = 500;

void plant(float actuator){
 //plant functions go here
    int A_fan = actuator; //actuator value
    int M_fan = 500; //fan's power

    int F_fan = 0;

    int ball_m = 1.0; //ball's mass
    int ball_a; //ball's acceleration
    int ball_v; //ball's velocity
    int ball_p; //ball's position
    int ball_f;


     F_fan = M_fan*A_fan;
    
     ball_a = (F_fan/1.0)-g;

     ball_v = ball_v + (ball_a*dt);

     ball_p = ball_p + (ball_v*dt);

 
     actual = ball_p;
}

enum pid_states{pid_init, pid_on, pid_output} pid_state;
int pid_tick(int state){
 switch(pid_state){ //transitions
   case pid_init:
      pid_state = pid_on;
      break;
   case pid_on:
      pid_state = pid_on;
   default:
      pid_state = pid_init;
      break;
 }
 switch(pid_state){ //state actions
   case pid_init:
      break;
   case pid_on:
      
      error = desired - actual;
      
      deriv = actual - actual_prev;
      actual_prev = actual;
      
      integral = integral + error;
      if(integral > 255){
         integral = 255;
      }
      if(integral < 0){
         integral = 0;
      }
      
      printf("Error: %d, Deriv: %d, Integral: %d\n", error, deriv, integral);
      actuator = CONST_P*error + CONST_I*integral - CONST_D*deriv;
     
      plant(actuator);
      
      break;
 }
   
}

enum manual_states{manual_init, manual_wait, manual_inc, manual_dec} manual_state;
int manual_tick(int state){
 switch(manual_state){ //transitions
   case manual_init:
      manual_state = manual_wait;
      break;
   case manual_wait:
      if(A6 && !A7){
         manual_state = manual_inc;
      }
      else if(!A6 && A7){
         manual_state = manual_dec;
      }
      else{
         manual_state = manual_wait;
      }
      break;
   case manual_inc:
      //TODO: If A6 and NOT A7, increase fan speed. Else, output then wait
      if(A6 && !A7){
         manual_state = manual_inc;
      }
      else if(!A6 && A7){
         manual_state = manual_dec;
      }
      else{
         manual_state = manual_wait;
      }
      break;
   case manual_dec:
      //TODO: If A7 and NOT A6, decrease fan speed. Else, output then wait
      if(A6 && !A7){
         manual_state = manual_inc;
      }
      else if(!A6 && A7){
         manual_state = manual_dec;
      }
      else{
         manual_state = manual_wait;
      }
      break;
   default:
      manual_state = manual_init;
 }
 switch(manual_state){ //state actions
   case manual_init:
      break;
   case manual_wait:
      printf("output for manual\n");
      break;
   case manual_inc:
      //TODO: increase fan speed
      actuator+=100;
      plant(actuator);
      break;
   case manual_dec:
      //TODO: decrease fan speed
      actuator-=100;
      plant(actuator);
      break;
 }
}


void output(){ //based on A1 input mode, output the actual height
   B = (actual)/255.0;
}

volatile int TimerFlag = 0;
void TimerISR() {
   TimerFlag = 1;
}


int main(){
   
   TimerSet(1000);
   TimerOn();
   while(1){
      //B0 = !B0; // Delete this of course. Call your PID controller and plant tick functions instead.
      //TODO: If NOT A0, call pid_tick
      //If A0, call manual_tick
      
      if(A0){
         manual_tick(manual_init);
      }
      else if(!A0){
         pid_tick(pid_init);
      }
      output();
      
      while(!TimerFlag);
      TimerFlag=0;
   }
}

