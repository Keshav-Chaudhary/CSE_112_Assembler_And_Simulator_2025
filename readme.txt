This project focuses on developing a Simple assembler for RISC-V assembly code that converts assembly instructions into binary machine code.
This assembler is built using Python and supports multiple RISC-V instruction types, such as R-type, I-type, S-type, B-type, U-type, and J-type instructions.
The work is organized into several tasks, with each task assigned to different group members.

The project is organized as follows:

RISC-V Assembler
├── input.asm            # Input assembly file
├── output.mc            # Output binary file
├── assembler.py         # Main Python code for the assembler
├── readme.txt           # Project documentation

Individual Contributions:

Ayan Ahmed ------>
1. Implemented the opcode() function 
    ○ Determine the opcode based on the instruction type (R-type, I-type, S-type, B-type, etc.). 
    ○ Return the appropriate opcode as a binary string.
2. Implemented the funct3() function  
    ○ Determine the funct3 field for instructions that require it (e.g., R-type, I-type, etc.). 
    ○ Return the appropriate 3-bit binary string. 
3. Implemented the funct7() function 
    ○ Determine the funct7 field for instructions that require it (e.g., R-type). 
    ○ Return the appropriate 7-bit binary string. 
4. Tested the functions 
    ○ Write test cases to ensure the functions correctly identify opcodes, funct3, and funct7 for various instruction types.

Pulkit Kumar ------>
1. Implemented the register_code() function 
    ○ Convert register names (e.g., x0, x1, ra, sp) to their 5-bit binary representation. 
    ○ Handle all 32 registers as per the RISC-V specification. 
2. Implemented the imm() function 
    ○ Convert immediate values to their binary representation based on the instruction type (e.g., I-type, S-type, B-type, etc.). 
    ○ Handle sign extension and padding as required. 
3. Test the functions 
    ○ Write test cases to ensure correct conversion of register names and immediate values.

Keshav and Sonu Paswan ------>
Processed labels in the assembly code and wrote the final binary output and testing along with integrating the overall logic to the main function.
1. Implemented the processor_labels() function 
    ○ Process labels in the assembly code and replace them with memory addresses or relative offsets. 
    ○ Handle both forward and backward references to labels. 
2. Implemented the write_to_bin() function 
    ○ Write the binary-encoded instructions to the output file in the correct format. 
3. Implemented the ovr_write_to_bin() function 
    ○ Ensure the output file is cleared before writing new binary code. 
4. Test the functions 
    ○ Write test cases to ensure labels are correctly processed and the binary output is written correctly.   

The RISC-V Simple Assembler successfully converts the assembly language into binary machine code, it supports different instruction types and allows us to create custom instructions.
Important functions like instruction parsing, register management, immediate value encoding, label processing, and writing binary files were successfully implemented as a result of the group collaborative approach.
The project is organized, with distinct roles assigned to each team member, and it also alingns with our plan for future improvements to enhance its functionality and user experience.











