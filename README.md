# CO_Project_2024

Assignment Description

In this project, we will implement a subset of RV32I (RISC-V 32-bit integer) instruction set. 
RISC-V, an open-source ISA, is increasingly used for open-source hardware development.

Assembler
We programmed an assembler for the aforementioned ISA and assembly. The assembler read the
assembly program as an input text file (stdin) and must generate the binary (if there are no errors)
as an output text file (stdout). If there are errors, the assembler  generate the error notifications
along with the line number on which the error was encountered as an output text file (stdout). In
case of multiple errors, the assembler may print an error.
The input to the assembler is a text file containing the assembly instructions. Each line of the
text file may be of one of two types:
1. Empty line: Ignore these lines
2. An instruction
3. A label
