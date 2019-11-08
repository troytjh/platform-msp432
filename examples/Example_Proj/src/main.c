#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//stores Admin log in information
struct log_in {
    char user[21];
    char pass[21];
};

//stores remaining inventory
struct inventory {
    int Amoxil;
    int Vicodin;
    int Tylenol;
    int Zestril;
};

//compares user input to admin log in 
void Authentication(char admin_user[], char admin_pass[]);

//handles which operation to perform
void Menu(struct inventory inv);

//diplays the remaining inventory
void Check_Quantity(struct inventory disp);

//restocks quantity of drugs available
void Refill(int *amox, int *vic, int *tyl, int *zes);

//removes drug quantities from inventory
void Dispense(int *amox, int *vic, int *tyl, int *zes);

int main() {
    //assigns admin log in
    struct log_in Admin;
    strcpy(Admin.user,"Admin20");
    strcpy(Admin.pass,"L3tM3in");
    //prompts user to log in
    Authentication(Admin.user,Admin.pass);

    //creates an instance of the drug inventory
    struct inventory drugs = {100,20,90,50};
    Menu(drugs);    
}

void Authentication(char admin_user[], char admin_pass[]) {
    char user_input[21], pass_input[21];
    int invalid=1;  
    //continues to prompt the user until correct log in is provided
    while(invalid) {
        printf("Enter Username:"); scanf("%21s%*[^\n]",user_input);
        printf("Enter Password:"); scanf("%21s%*[^\n]",pass_input);

        (strcmp(admin_user,user_input)) ? printf("\nIncorrect username or password\n\n\r") :
        (strcmp(admin_pass,pass_input)) ? printf("\n\nIncorrect username or password\n\n\r") :
        (invalid=0); //signifies user input for user name and password were the same as admin log in
    }
}

void Menu(struct inventory inv) {
    int *amox=&inv.Amoxil, *vic=&inv.Vicodin, *tyl=&inv.Tylenol, *zes=&inv.Zestril;

    int choice=0, cont=1, flag=1;
    //continues while variable cont is true
    while(cont) {
        printf("\n\n\tDrug Inventory\n\n\r");
        printf("1. Check Quantity\n\r2. Refill\n\r3. Dispense\n\r4. Quit\n\n\r");

        printf("Select Option:");
        do {
            scanf("%i",&choice);
            switch(choice) {
                case 1:
                    Check_Quantity(inv);
                    /*signifies a valid case was selected, executed, 
                    and the menu text should be redisplayed*/
                    flag=0; 
                    break;
                case 2:
                    Refill(amox, vic, tyl, zes);
                    flag=0;
                    break;
                case 3:
                    Dispense(amox, vic, tyl, zes);
                    flag=0;
                    break;
                case 4:
                    printf("Program Done.\n\r");
                    cont=0; flag=0;
                    break;
                //occurs if input does not match one of the cases
                //variable flag is set to reprompt user for input
                default :
                    printf("\nEnter a number between 1-4\n\r");
                    flag=1;
                    break;

            }
        }while(flag);
    }

}

void Check_Quantity(struct inventory disp) {
    printf("\n\tCurrent Quantities\n\n\r");
    printf("Amoxil %i\nVicodin %i\nTylenol %i\nZestril %i\n\n\r", 
        disp.Amoxil, disp.Vicodin, disp.Tylenol, disp.Zestril);
    
    char b='\0'; 
    printf("Return to menu bress b\n\r");
    while(b!='b') { scanf(" %c",&b); }
}

void Refill(int *amox, int *vic, int *tyl, int *zes) {
    int refill=0, choice=0, cont=1;
    printf("\nRefill which drug\n\n\r");
    printf("1.Amoxil\n2.Vicodin\n3.Tylenol\n4.Zestril\n\r");
    
    while(cont) {
        scanf("%i",&choice);
        switch(choice) {
            case 1:
                printf("Enter refill amount:");
                scanf("%i",&refill);
                *amox+=refill;
                cont=0;
                break;
            case 2:
                printf("Enter refill amount:");
                scanf("%i",&refill);
                *vic+=refill;
                cont=0;
                break;
            case 3:
                printf("Enter refill amount:");
                scanf("%i",&refill);
                *tyl+=refill;
                cont=0;
                break;
            case 4:
                printf("Enter refill amount:");
                scanf("%i",&refill);
                *zes+=refill;
                cont=0;
                break;
            default :
                printf("\nEnter a number between 1-4\n\r");
                cont=1;
                break;
        }
    }
}

void Dispense(int *amox, int *vic, int *tyl, int *zes) {
    int dispense=0,choice=0, cont=1; char ans='y';
    printf("\nDispense which drug?\n\n\r");
    printf("1.Amoxil\n2.Vicodin\n3.Tylenol\n4.Zestril\n\r");

    
    while(cont) {
        scanf("%i",&choice);
        switch(choice) {
            case 1:
                //repeats input request if invalid amount and y is selected
                ans='y';
                while(ans=='y') {
                    printf("Enter dispense amount:");
                    scanf("%i",&dispense);
                    *amox-=dispense; //reduces drug inventory by amount specified

                    if(*amox<0) {
                        //reverts drug to valid quantity
                        *amox+=dispense; dispense=0;
                        printf("Not enough quantity\nRedispense? y or n\n\r");
                        scanf(" %c",&ans);
                        if(ans=='n') { cont=0; }
                    }
                    else { ans='n'; cont=0;}
                }
                break;
            case 2:
                ans='y';
                while(ans=='y') {
                    printf("Enter dispense amount:");
                    scanf("%i",&dispense);
                    *vic-=dispense;

                    if(*vic<0) {
                        *vic+=dispense; dispense=0;
                        printf("Not enough quantity\nRedispense? y or n\n\r");
                        scanf(" %c",&ans);
                        if(ans=='n') { cont=0; }
                    }
                    else { ans='n'; cont=0; }
                }
                break;
            case 3:
                ans='y';
                while(ans=='y') {
                    printf("Enter dispense amount:");
                    scanf("%i",&dispense);
                    *tyl-=dispense;

                    if(*tyl<0) {
                        *tyl+=dispense; dispense=0;
                        printf("Not enough quantity\nRedispense? y or n\n\r");
                        scanf(" %c",&ans);
                        if(ans=='n') { cont=0; }
                    }
                    else { ans='n'; cont=0; }
                }
                break;
            case 4:
                ans='y';
                while(ans=='y') {
                    printf("Enter dispense amount:");
                    scanf("%i",&dispense);
                    *zes-=dispense;

                    if(*zes<0) {
                        *zes+=dispense; dispense=0;
                        printf("Not enough quantity\nRedispense? y or n\n\r");
                        scanf(" %c",&ans);
                        if(ans=='n') { cont=0; }
                    }
                    else { ans='n'; cont=0; }
                }
                break;
            default :
                printf("\nEnter a number between 1-4\n\r");
                cont=1;
                break;
        }
    }
}
