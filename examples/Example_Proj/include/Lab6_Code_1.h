#ifndef FUNC
#define FUNC

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct patient_info {
    char name[21];
    int nyha;
    int walk_dist;
    float ef;

    int eligible;
};

//assigns patient data to the struct array of patients
void Patient_Data(struct patient_info p_data[]);

//checks the patient data against CRT requirements and assigns eligibility
struct patient_info CRT_Eligible(struct patient_info p[], int i);

void Display_Eligibility(struct patient_info patient[]);

#endif