/* 
* Lab Partner Names:
* Lab #:
*/

/*Include files */
#include <stdio.h>
#include <stdlib.h>
#include "Lab6_Code_1.h"

/*Function Declarations*/
void OutputInit(void); 

int main(void)
{
    /*Setup Launchpad for Printf & Scanf*/
		OutputInit(); 
		
		/* Place application code here */
	struct patient_info patient[4];
	Patient_Data(patient);

  //define the size of the array
  int len=4;
  CRT_Eligible(patient, --len);

  Display_Eligibility(patient);
		
	/*Go in waiting state. Will modify in later labs*/
	while(1);
 }
