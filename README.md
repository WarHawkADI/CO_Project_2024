# CO_Project_2024

Assignment Description

In this project, we will implement a subset of RV32I (RISC-V 32-bit integer) instruction set. 
RISC-V, an open-source ISA, is increasingly used for open-source hardware development.

Assembler

We programmed an assembler for the aforementioned ISA and assembly. The assembler read the
assembly program as an input text file (stdin) and generate the binary (if there are no errors)
as an output text file (stdout). If there are errors, the assembler  generate the error notifications
along with the line number on which the error was encountered as an output text file (stdout). In
case of multiple errors, the assembler may print an error.
The input to the assembler is a text file containing the assembly instructions. Each line of the
text file may be of one of two types:
1. Empty line: Ignore these lines
2. An instruction
3. A label


Here is the meaning corresponding to these entities.
1. An instruction can be of the following:
The opcode from the mentioned mnemonics.
A register can be zero, ra, sp, gp, etc. as per their ABI Name.
A immediate within bounds as per specified instruction.
A label thet will be utilized at jump and branch type instructions.

8

2. If an instruction is labeled. Then, the label must be at the beginning of the instruction. The
label is followed by a colon with no space in between the label and the colon. The branch
instructions in the assembly code will utilize the labels to jump to the specific location. While
converting assembly into binary, the label will be converted into an immediate by subtracting

the absolute instruction address (pointed out by the label) from the current instruction ad-
dress (Program Counter). The arithmetic operation is signed as the jump can be upward or

downward. And, the converted immediate is signed (2’s complement representation) and is of
12 bits.
All the programs should terminate with the Virtual Halt instruction (beq zero,zero,0x00000000).
Note that the immediate is signed. Here (0x00000000) represents (0) of decimal. This instruction
can be used to halt the processor. The assembler should be capable of:
1. Handling all supported instructions
2. Making sure that any illegal instruction (any instruction (or instruction usage) that is not
supported) results in a syntax error. In particular, you must handle:
(a) Typos in instruction or register name
(b) Flag illegal immediate whose length goes out of bounds as per the available length in the
instruction.
(c) Missing Virtual Halt instruction
(d) Virtual Halt not being used as the last instruction
3. The corresponding binary is generated if the code is error-free. The binary file is a text file in
which each line is a 32-bit binary number written using 0s and 1s in ASCII.
Note: ABI stands for Application Binary Interface.
