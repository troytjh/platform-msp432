#===============================================================
#Makefile for building MSP Code Examples in command line
#environement using the GCC Open Source Compiler for MSP432
#===============================================================

# Require DEVICE to be specified
ifndef DEVICE
$(info Please specify a device, e.g. DEVICE=MSP432P401R)
$(error unspecified device)
endif

OBJ_DIR			:= output

###################### Windows OS ######################
ifeq ($(OS),Windows_NT)
	################## GCC Root Variable ###################
	INSTALL_DIR 		:= ../../..
	GCC_MSP_INC_DIR 	?= $(INSTALL_DIR)/arm/include
	GCC_CMSIS_INC_DIR 	?= $(GCC_MSP_INC_DIR)/CMSIS
	LDDIR				:= $(GCC_MSP_INC_DIR)/$(DEVICE)
	ifneq (,$(findstring cygwin, $(PATH)))
		RM					:= rm -rf
		MKDIR				= mkdir -p -- $@
	else
		RM					:= rd /s /q
		MKDIR				= mkdir
	endif
################### Linux or Mac OS ####################
else
	OS 					:= $(shell uname)
	################## GCC Root Variable ###################
	INSTALL_DIR			:= ../../..
	GCC_MSP_INC_DIR 	?= $(INSTALL_DIR)/arm/include
	GCC_CMSIS_INC_DIR 	?= $(GCC_MSP_INC_DIR)/CMSIS
	LDDIR				:= $(GCC_MSP_INC_DIR)/$(shell echo $(DEVICE) | tr A-Z a-z)
	RM					:= rm -rf
	MKDIR				= mkdir -p -- $@
endif

######################################
GCC_BIN_DIR		?= $(INSTALL_DIR)/arm_compiler/bin/
GCC_INC_DIR		?= $(INSTALL_DIR)/arm_compiler/arm-none-eabi/include
######################################
CC              := $(GCC_BIN_DIR)arm-none-eabi-gcc
GDB			    := $(GCC_BIN_DIR)arm-none-eabi-gdb
######################################
INCLUDES		:= -I $(GCC_CMSIS_INC_DIR) -I $(GCC_MSP_INC_DIR) -I $(GCC_INC_DIR)
CFLAGS			:= -mcpu=cortex-m4 -march=armv7e-m -mfloat-abi=hard -mfpu=fpv4-sp-d16 -mthumb -D__$(DEVICE)__ -DTARGET_IS_MSP432P4XX -Dgcc -g -gstrict-dwarf -Wall -ffunction-sections -fdata-sections -MD -std=c99
LDFLAGS			:= -mcpu=cortex-m4 -march=armv7e-m -mfloat-abi=hard -mfpu=fpv4-sp-d16 -mthumb -D__$(DEVICE)__ -DTARGET_IS_MSP432P4XX -Dgcc -g -gstrict-dwarf -Wall -T$(LDDIR).lds -l'c' -l'gcc' -l'nosys'

######################################

ifeq ($(DEVICE), MSP432P401R)
	STARTUP			:= startup_msp432p401r_gcc
	SYSTEM			:= system_msp432p401r
else
	STARTUP			:= startup_msp432p401m_gcc
	SYSTEM			:= system_msp432p401m
endif
SRC_FILE		:= msp432p401_blinkingLED

OBJECTS			:= $(OBJ_DIR)/$(SRC_FILE).o $(OBJ_DIR)/$(STARTUP).o $(OBJ_DIR)/$(SYSTEM).o
######################################
all: $(OBJ_DIR)/$(SRC_FILE).out

$(OBJECTS): | $(OBJ_DIR)

$(OBJ_DIR):
	@$(MKDIR) $(OBJ_DIR)

$(OBJ_DIR)/%.o: %.c
	@echo ============================================
	@echo Generating $@
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

$(OBJ_DIR)/$(SRC_FILE).out: . $(OBJECTS)
	@echo ============================================
	@echo Linking objects and generating output binary
	$(CC) $(LDFLAGS) $(word 2,$^) $(OBJ_DIR)/$(STARTUP).o $(OBJ_DIR)/$(SYSTEM).o -o $@ $(INCLUDES)

debug: all
	$(GDB) $(OBJ_DIR)/$(SRC_FILE).out

clean:
	@$(RM) $(OBJ_DIR)