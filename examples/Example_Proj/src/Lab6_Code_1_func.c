#include "Lab6_Code_1.h"

void Patient_Data(struct patient_info p_data[]) {
    char *p_name[] = {"Bev Blackwell", "Kohen Miles", "Emilio Dean", "Elen Boone"};
    int p_nyha[]={3,4,2,3}, p_dist[]={250,170,210,200}; 
    float p_ef[]={0.3,0.25,0.4,0.33};

    for(int i=0;i<4;++i) {
        strcpy(p_data[i].name,*(p_name+i));
        p_data[i].nyha=p_nyha[i];
        p_data[i].walk_dist=p_dist[i];
        p_data[i].ef=p_ef[i];
    }
}

struct patient_info CRT_Eligible(struct patient_info p[], int i) {        
    if(p[i].nyha<3) { p[i].eligible=0; }
    else if(p[i].walk_dist>225) { p[i].eligible=0; }
    else if(p[i].ef>.35) { p[i].eligible=0; }
    else { p[i].eligible=1; }

    if(i>0) { return CRT_Eligible(p, --i); }
    else { return *p; }   
}

void Display_Eligibility(struct patient_info patient[]) {
    for(int i=0;i<4;++i) {
        if(patient[i].eligible) {
            printf("Patient %s is eligible for CRT\n\r", patient[i].name);
        }
    }
}
