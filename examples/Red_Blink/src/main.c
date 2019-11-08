//place header files as needed
#include "msp.h"
#include "Lab7_Code_3.h"

int main(void) {
	//place code that runs once
	int out[] = {0x01,0x01};
	int del = 75000;

	int rgb = 0x01;
    while(1) {
        //place code to execute repeatedly
	*(out+0) = 0x01; *(out+1)=0x01;
	Led1(out[0]);
	Led2(rgb, out[1]);
	
	delay(del);
			
	*(out+0) = 0x00; *(out+1)=0x00;
	Led1(out[0]);
	Led2(rgb, out[1]);
		
	delay(del);
    }
}
