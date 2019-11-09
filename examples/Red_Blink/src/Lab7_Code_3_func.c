#include "Lab7_Code_3.h"

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
