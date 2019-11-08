//place header files as needed
#include "msp432p401r.h"

void Led1(int o);

void Led2(int i, int o);

void Led_Reset(void);

void delay(int d);


int main(void) {
    //place code that runs once
		int out = 0x01;
		int del = 750000;

		int rgb = 0x01;
		
    while(1) {
        //place code to execute repeatedly
				Led2(rgb,out);
				delay(del);
				++rgb; ++out;
			
				Led_Reset();
				if(rgb==0x08) { rgb=0x01; out=0x01; }
    }
}


void Led1(int o) {
		P1->SEL0 &= ~0x01;
	P1->SEL1 &= ~0x01;
	
    P1->DIR  |= 0x01;
		(o) ? (P1->OUT|=o) : (P1->OUT&=o);
}

void Led2(int i, int o) {
		P2->SEL0 &= ~0x02;
		P2->SEL1 &= ~0x02;
	
	  P2->DIR |= i;
	  (o) ? (P2->OUT|=o) : (P2->OUT&=o);
}

void delay(int d) {
	for (int i=0; i<d; ++i) { }
}

void Led_Reset(void) {
		P2->OUT &=0x00;
}

