//place header files as needed
#include "msp432p401r.h"

int main(void) {
    //place code that runs once
		P1->SEL0 &= ~0x01;
	  P1->SEL1 &= ~0x01;
	
    P1->DIR  |= 0x01;
	  P1->OUT |= 0x01;
	
    while(1) {
        //place code to execute repeatedly

    }
}
