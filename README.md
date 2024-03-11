# CO_Project_2024


## Overview

This repository contains a lightweight RISC-V assembler implemented in Python. The assembler translates RISC-V assembly code into machine code, enabling execution on a RISC-V architecture. The primary goal is to provide a simple yet functional tool for converting human-readable assembly instructions into the binary format understood by RISC-V processors.

## Features

### Instruction Support

The assembler covers a range of RISC-V instructions, organized into different types:

- **R-Type Instructions:**
  - `add`, `sub`, `sll`, `slt`, `sltu`, `xor`, `srl`, `or`, `and`

- **I-Type Instructions:**
  - `lw`, `addi`, `sltiu`, `jalr`

- **S-Type Instructions:**
  - `sw`

- **B-Type Instructions:**
  - `beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu`

- **U-Type Instructions:**
  - `lui`, `auipc`

- **J-Type Instructions:**
  - `jal`

### Label Support

The assembler handles labels for branch and jump instructions, enhancing code organization and readability. Labels allow for more expressive and structured assembly code, especially in the context of control flow instructions.

### Error Handling

The assembler provides informative error messages for common issues encountered during the assembly process. Key error scenarios and their corresponding error codes include:

1. **Unknown Instruction Used (Error Code: 1):** The assembler encounters an unknown instruction in the provided assembly code.
2. **Unknown Register Used (Error Code: 2):** An undefined register is referenced in the assembly code.
3. **Illegal Immediate Value (Error Code: 3):** An immediate value exceeds the allowable range for the given instruction.
4. **Virtual Halt Is Missing (Error Code: 4):** The assembler detects that a virtual halt instruction is missing, ensuring proper program termination.

## License

This RISC-V Assembler is licensed under the MIT License, permitting users to freely use, modify, and distribute the code. For detailed information, refer to the [LICENSE](LICENSE) file. If you encounter any issues or have suggestions for improvement, please feel free to open an [issue](https://github.com/your-username/riscv-assembler/issues).


