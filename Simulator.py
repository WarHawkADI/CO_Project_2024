import sys
R_op_code= {"add":"0110011","sub":"0110011","sll":"0110011","slt":"0110011",
"sltu":"0110011","xor":"0110011","srl":"0110011","or":"0110011","and":"0110011"}

I_op_code= {"lw":"0000011", "addi":"0010011", "sltiu":"0010011", "jalr":"1100111"}

S_op_code= {"sw":"0100011"}

B_op_code= {"beq":"1100011", "bne":"1100011","blt":"1100011",
"bge":"1100011", "bltu":"1100011", "bgeu":"1100011"}

U_op_code= {"lui":"0110111", "auipc": '0010111'}

J_op_code= {"jal":"1101111"}

registers= {"zero":"00000", "ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101",
"t1":"00110","t2":"00111","s0":"01000","fp": "01000","s1": "01001", "a0":"01010", "a1": "01011",
 "a2":"01100", "a3": "01101", "a4":"01110", "a5": "01111", "a6": "10000", "a7":"10001",
 "s2": "10010", "s3":"10011", "s4":"10100","s5":"10101", "s6":"10110", "s7":"10111",
 "s8":"11000" ,"s9": "11001", "s10":"11010", "s11": "11011" ,
 "t3":"11100", "t4":"11101", "t5":"11110", "t6":"11111"}  



def binary_to_decimal(binary_str, bits, is_twos_complement=True):
    val = int(binary_str, 2)
    if is_twos_complement and (val & (1 << (bits - 1))): 
        val -= (1 << bits)  
    return val
def unsigned(num1, bits):
    return binary_to_decimal(decimal_to_binary(num1, bits-1), bits, False)

memory={}
for i in range(0,32):
    memory[4*i +65536]= 0

def decimal_to_binary(decimal, num_bits):
    binary = bin(decimal & ((1 << num_bits) - 1))[2:] 
    binary = '0' * (num_bits - len(binary)) + binary 
    return binary




registers={"00000":0,"00001":0,"00010":256,"00011":0,"00100":0,"00101":0,"00110":0,"00111":0,
           "01000":0, "01001":0,"01010":0, "01011":0,
           "01100":0, "01101":0,"01110":0, "01111":0,
            "10000":0,"10001":0, "10010":0,"10011":0,"10100":0,"10101":0,"10110":0,"10111":0,
            "11000":0, "11001":0,"11010":0, "11011":0 ,"11100":0,"11101":0,"11110":0,"11111":0}  
inputFile=sys.argv[1]
outputFile= sys.argv[2]
file=open(inputFile,'r')
text=file.read()

text=text.split('\n')
file.close()
f1= open(outputFile,'w')

PC=0
count1=0
while PC<=128:
    count1+=1
    if count1>=49:
        break
    line= text[PC//4]
    line=line.strip()
    if line[-7:]=='1111111' or '00000000000000000000000001100011' in line : 
        registers["00000"]=0
        registers_output = " ".join([f"0b{decimal_to_binary(registers[decimal_to_binary(i, 5)], 32)}" for i in range(0, 32)])
        output = f"0b{decimal_to_binary(PC, 32)} {registers_output}\n"
        f1.write(output)
        break
    elif line[-7:] =="0110011":
        PC+=4
        opcode = line[-7:]
        funct3 = line[-15:-12]
        funct7 = line[-32:-25]
        rs1 = line[-20:-15]
        rs2 = line[-25:-20]
        rd = line[-12:-7]
        if funct3 == '000' and funct7 == '0000000': 
            registers[rd] = registers[rs1] + registers[rs2]
        elif funct3 == '000' and funct7 == '0100000': 
            registers[rd] = registers[rs1] - registers[rs2]
        elif funct3 == '001' and funct7 == '0000000':
            registers[rd]= registers[rs1]<<binary_to_decimal(decimal_to_binary(registers[rs2],5),5,False)  
        elif funct3 == '010' and funct7 == '0000000':
            if registers[rs1] < registers[rs2]:
                registers[rd]=1

        elif funct3 == '011' and funct7 == '0000000':
            if unsigned(registers[rs1],5) < unsigned(registers[rs2],5):
                registers[rd]=1
        elif funct3 == '100' and funct7 == '0000000':
            registers[rd]= registers[rs1] ^ registers[rs2]
        elif funct3 == '101' and funct7 == '0000000': 
            registers[rd]= registers[rs1]>> unsigned(registers[rs2],5)
        elif funct3== "110" and funct7 == '0000000': 
            registers[rd]= registers[rs1] | registers[rs2]
        elif funct3== "111" and funct7 == '0000000': 
            registers[rd]= registers[rs1] & registers[rs2]
        else:
                pass

    elif line[-7:] in U_op_code.values(): 
         opcode = line[-7:]
         PC+=4

         if opcode == '0110111': 
            imm = line[-32:-12] 
            rd = line[-12:-7] 
            imm_value = binary_to_decimal(imm, 32)
            registers[rd] = imm_value << 12
         elif opcode == '0010111': 
            imm = line[-32:-12]
            rd = line[-12:-7] 
            imm_value = binary_to_decimal(imm, 32)
            registers[rd] = PC + (imm_value << 12) -4
         
    elif line[-7:] in S_op_code.values(): 
         PC+=4
         imm= line[-32:-25]+ line[-12:-7]
         rs2= line[-25:-20]
         rs1= line[-20:-15]
         mem= registers[rs1]+ binary_to_decimal(imm,12)
         memory[mem]= registers[rs2]
            
    elif line[-7:] in J_op_code.values(): 
         imm= line[-32]+ line[-20:-12]+ line[-21]+line[-31:-21]
         rd=line[-12:-7]
         registers[rd]= PC+4
         PC+= binary_to_decimal(imm+"0", 21)
         PC= decimal_to_binary(PC,32)
         PC= PC[:-1]+"0"
        
         PC = int(PC,2)
            
    elif (line)[-7:] in B_op_code.values(): 
        PC+=4
        imm=""
        rs1= line[-20:-15]
        rs2= line[-25:-20]
        imm= line[-32]+line[-8]+ line[ -31:-25]+ line[-12:-8] +"0" 
        imm= binary_to_decimal( imm, 13)
        func3= line [-15:-12]
        if func3== "000": 
            if registers[rs1]==registers[rs2]:
                if rs1== "00000":
                    break  
                PC-=4                 
                PC+=imm
        elif func3== "001": 
            if registers[rs1]!=registers[rs2]:
                PC-=4
                PC+=imm
        elif func3== "100": 
            if registers[rs1] < registers[rs2]:
                PC-=4
                PC+= imm
        elif func3== "101": 
            if registers[rs1] >= registers[rs2]:
                PC-=4
                PC+= imm
        elif func3== "110": 
            if registers[rs1] < registers[rs2]:
                PC-=4
                PC+= imm
        elif func3== "111": 
            if registers[rs1] >= registers[rs2]:
                PC-=4
                PC+=imm
        else:
            pass
            
    elif line[-7:] in I_op_code.values(): 
         PC+=4
         funct3= line[-15:-12]
         rd= line[-12:-7]
         rs= line[-20:-15]
         imm= line[-32:-20]
         opcode= line[-7:]
         if opcode=="0000011" and funct3=="010":
             registers[rd]= memory[registers[rs1]+ binary_to_decimal(imm,12)]
         elif opcode=="0010011" and funct3== "000": 
             registers[rd]= registers[rs]+ binary_to_decimal(imm, 12)
         elif opcode== "0010011" and funct3== "011": 
             if unsigned(registers[rs],13) < unsigned(imm,13):
                 registers[rd]= 1
         elif opcode== "1100111" and funct3=="000": 
             registers[rd]= PC
             PC-=4
             PC= registers[rs]+ int(imm,2)
             PC= decimal_to_binary(PC,32)
             PC= PC[:-1]+"0"
            
             PC = int(PC,2)
             
         pass
            
    elif line[-7:] =="0000001": 
        rs2=line[-25:-20]
        rs1= line[-20:-15]
        rd= line[-12:-7]
        registers[rd]= binary_to_decimal(decimal_to_binary(registers[rs2]* registers[rs1],32),32)
    elif line[-7:]=="0000010": 
        for i in registers.values():
            i=0
        registers["00010"]=256
    elif line[-7:]== "0000100": 
        rs1= line[-20:-15]
        rd= registers[-12:-7]
        registers[rd]= binary_to_decimal((decimal_to_binary(registers[rs1],32))[::-1],32)


    else: 
        break
    registers["00000"]=0
    registers_output = " ".join([f"0b{decimal_to_binary(registers[decimal_to_binary(i, 5)], 32)}" for i in range(0, 32)])
    output = f"0b{decimal_to_binary(PC, 32)} {registers_output}\n"
    f1.write(output)
    
n=""
for i in (memory.keys()):
    mem_hex= format(i, f"0{8}X")
    n+=(f"0x{mem_hex.lower()}:0b{decimal_to_binary(memory[i],32)}\n")
f1.write(n)
f1.close()