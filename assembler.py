R_op_code= {"add":["0110011","000"],
            "sub":["0110011","000"],
            "sll":["0110011","001"],
            "slt":["0110011","010"],
            "sltu":["0110011","011"],
            "xor":["0110011","100"],
            "srl":["0110011","101"],
            "or":["0110011","110"],
            "and":["0110011","111"]}

I_op_code= {"lw":["0000011","010"], 
            "addi":["0010011","000"],
            "sltiu":["0010011","011"], 
            "jalr":["1100111","000"]}

S_op_code= {"sw":["0100011","010"]}

B_op_code= {"beq":["1100011","000"], 
            "bne":["1100011","001"],
            "blt":["1100011","100"],
            "bge":["1100011","101"], 
            "bltu":["1100011","110"], 
            "bgeu":["1100011","111"]}

U_op_code= {"lui":"0110111", 
            "auipc": '0010111'}

J_op_code= {"jal":"1101111"}

PC=0

function_list= {"R":["add","sub","sll","slt","sltu","xor","srl","or","and"],
                "I":["lw","addi","sltiu","jalr"], 
                "S":["sw"], 
                "B":["beq","bne","blt","bge","bltu","bgeu"],
                "U":["lui","auipc"], 
                "J":["jal"]}


registers= {"zero":"00000", 
            "ra":"00001",
            "sp":"00010",
            "gp":"00011",
            "tp":"00100",
            "t0":"00101",
            "t1":"00110",
            "t2":"00111",
            "s0":"01000",
            "fp": "01000",
            "s1": "01001", 
            "a0":"01010", 
            "a1": "01011",
            "a2":"01100", 
            "a3": "01101", 
            "a4":"01110", 
            "a5": "01111", 
            "a6": "10000", 
            "a7":"10001",
            "s2": "10010", 
            "s3":"10011", 
            "s4":"10100",
            "s5":"10101", 
            "s6":"10110", 
            "s7":"10111",
            "s8":"11000" ,
            "s9": "11001", 
            "s10":"11010", 
            "s11": "11011" ,         
            "t3":"11100", 
            "t4":"11101", 
            "t5":"11110", 
            "t6":"11111"}                                        

errors= {1:"Unknown instruction used", 
         2: "Unknown register used", 
         3:"Illegal immediate value",
        4:"Virtual halt is missing"}

def flip(val):
    return '1' if (val == '0') else '0'

def d2b(num):
    pbin = '{0:b}'.format(num)
    return pbin

def twocomp(num,bits):
    if num >= 0:
        ans = d2b(num)
        return ans.zfill(bits)
    else:
        pnum = abs(num)
        neg = d2b(pnum)
        temp = 0
        for i in range(len(neg)-1,0,-1):
            if neg[i] == "1":
                temp = i
                break
            else:
                continue
        for j in range(0,temp):
            neg = neg[:j] + flip(neg[j]) + neg[j+1:]
        return neg.rjust(bits,"1")

def binaryToDecimal(val_str, bits):

    val = int(val_str, 2)
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

def checkDigit(st):
    st=str(st)
    if st.isdigit():
        return True
    elif st[0]=='-' and st[1:].isdigit():
        return True
    else:
        return False

labels={0:1}

def findLabel(startLine, allLines):
    count=0
    label=""
    for i in range(len(allLines)):
        if allLines[i]!=startLine:
            continue
        count=i
        label= (startLine.split(','))[-1]
        break
    i=0
    while ( i<len(allLines)):
        if allLines[i][:len(label)]== label:
            break
        i+=1
    if (i==len(allLines)):
        return
    else:
        return 4*(i-count)

def R_instruction(line):            
    output=""
    instruction= line.split()[0]
    if instruction=='sub':
        output="0100000"
    else:
        output="0000000"
    registers_index= (line.split()[1]).split(',')
    for r in registers_index[-1:0:-1]:
        if r not in registers.keys():
            raise Exception(f"{r} register not found")

        else:
            for key,val in registers.items():
                if key== r:
                    output+=val
                    break

    for ins in R_op_code.keys():
        if ins==instruction:
            output+= R_op_code[ins][1]

    rd= registers_index[0]
    if rd not in registers.keys():
        raise Exception(f"{rd} register not found")

    output+= registers[rd]
    output+= "0110011"

    return output

def J_instruction(line,allLines):  
    global labels
    global PC
    r1= ((line.split())[1].split(','))[0]
    if r1 not in registers.keys():
        raise Exception(f"{r1} register not found")
    j_register= registers[r1]
    labelName= ((line.split())[1].split(','))[-1]
    if labelName[-1]=='\n':
        labelName=labelName[:-1]
    if checkDigit(labelName):
        immBinary= twocomp(int(labelName),21)
    else:
        imm= findLabel(line, allLines )  
        immBinary= twocomp(imm,21)  
        labels[(line.split(','))[-1]]= imm
    PC1= immBinary[0:-1]+'0'     
    PC_temp= binaryToDecimal(PC1,21)  
    PC+=PC_temp                       
    output= f"{immBinary[0]}{immBinary[10:20]}{immBinary[9]}{immBinary[1:9]}{j_register}1101111"
    return output

def B_instruction(line,allLines):          
    global PC
    global labels
    instruction_name=line.split()[0]
    registerNames=((line.split())[1].split(','))[0:2]
    labelName= (line.split(','))[-1]
    if labelName[-1]=='\n':
        labelName=labelName[:-1]
    if checkDigit(labelName):
        immBinary= twocomp(int(labelName),21)
    else:
        imm= findLabel(line ,allLines)
        immBinary= twocomp(imm,13)
        labels[(line.split(','))[-1]]= imm
    output= f"{immBinary[0]}{immBinary[-11:-5]}"

    for r in registerNames[::-1]:
        if r not in registers.keys():
            raise Exception(f"{r} register not found")

        else:
            output+=registers[r]
    if instruction_name not in B_op_code.keys():
        raise Exception(f"{instruction_name} instruction not found")

    output+= B_op_code[instruction_name][1]
    output+=f"{immBinary[-5:-1]}{immBinary[0]}"
    output+="1100011"
    return output

def U_instruction(line):
    components = line.split()
    opcode = components[0]
    if opcode not in U_op_code.keys():
        raise Exception("Instruction not found")

    destination_register = components[1].split(',')[0]

    if destination_register not in registers.keys():
        raise Exception("register not found")

    immediate = components[1].split(',')[1]
    immediate = int(immediate)
    if immediate>2**31 -1 or immediate< -(2**31):
        raise Exception("Immediate overflow")
    immediate_binary=twocomp(immediate,32)

    output=immediate_binary[0:20]
    output+=registers[destination_register]
    output+= U_op_code[opcode]
    print(output)
    return output

def S_instruction(line):
    output=''
    opcode='0100011'
    funct3='010'
    instruction=line.split()[0]
    rs2=(line.split()[1]).split(',')[0]

    rs1= (line.split()[1]).split(',')[1].split('(')[1][:-1]
    imm = int(line.split()[1].split(',')[1].split('(')[0])
    if rs1 and rs2 in registers.keys():
        rs1binary=registers[rs1]
        rs2binary=registers[rs2]
    else:
        raise Exception("register not found")
    immbinary = twocomp(imm,12)
    output+=immbinary[0:7]
    output+=rs2binary
    output+=rs1binary
    output+=funct3
    output+=immbinary[7:]+opcode
    return output

def I_instruction(line, allLines):
    global PC
    global labels
    inst_name=line.split()[0]
    rd=line.split()[1].split(',')[0]
    rs=line.split()[1].split(',')[1]
    if inst_name=="lw":
        rs=line.split()[1].split(',')[1].split('(')[1][0:-1]
        imm= int(line.split()[1].split(',')[1].split('(')[0])
    else:
        imm=(line.split()[1].split(',')[2])
    if inst_name not in I_op_code.keys():
        raise Exception("Instruction name invalid")
    if rs not in registers.keys() :
        raise Exception(f"Register not found {rs}" )
    if rd not in registers.keys():
        raise Exception(f"Register not found {rd}" )
    if (checkDigit(imm)):
        imm=int(imm)
        if ((imm>2**11-1 or imm<-(2**11)) and inst_name!="sltiu"):
            raise Exception("Overflow")
        elif (inst_name=="sltiu" and (imm>2**12-1 or imm<-(2**12))):
            raise Exception("Overflow")
        immBinary= twocomp(imm,12)
    else:
        labelName=imm
        imm= findLabel(line,allLines)
        immBinary= twocomp(imm,12)  
        labels[labelName]= imm
    output= immBinary[:12]+registers[rs]
    output+= I_op_code[inst_name][1]+ registers[rd]+I_op_code[inst_name][0]
    return output

input=open("Input.txt",'r')

text=input.read()
input.close()
output= open("Output.txt", 'w')
flag=False
text= text.split('\n')
for line in text :
    if line!="":
        if ':' in line:
            line=line.split(':')[1]
        instruction_name=line
        instruction_name= instruction_name.split()
        for (key,val) in function_list.items():
            if instruction_name[0] in val:
                
                if key== "R":
                    print(line)
                    output.write(R_instruction(line))
                elif key== "I":
                    print(line)
                    output.write(I_instruction(line,text))
                elif key== "S":
                    print(line)
                    output.write(S_instruction(line))
                elif key== "B":
                    print(line)
                    l1=B_instruction(line,text)
                    print(l1)
                    output.write(l1)
                elif key== "U":
                    print(line)
                    l1=U_instruction(line)
                    print(l1)
                    output.write(U_instruction(line))
                elif key== "J":
                    print(line)
                    output.write(J_instruction(line, text) )
                else:
                    raise Exception("Instruction is not found")
                output.write('\n')
                if flag==1:
                    PC+=4
output.close()

