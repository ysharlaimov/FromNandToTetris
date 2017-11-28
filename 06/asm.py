# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 21:49:20 2017

@author: sharl
"""
comp = {
        "0"   : 0b0101010,
        "1"   : 0b0111111,
        "-1"  : 0b0111010,
        "D"   : 0b0001100,   
        "!D"  : 0b0001101,
        "-D"  : 0b0001111,
        "D+1" : 0b0011111,
        "D-1" : 0b0001110,
        
        "A"   : 0b0110000,
        "!A"  : 0b0110001,
        "-A"  : 0b0110011,
        "A+1" : 0b0110111,
        "A-1" : 0b0110010,
        "D+A" : 0b0000010,
        "D-A" : 0b0010011,
        "A-D" : 0b0000111,
        "D&A" : 0b0000000,
        "D|A" : 0b0010101,            

        "M"   : 0b1110000,
        "!M"  : 0b1110001,
        "-M"  : 0b1110011,
        "M+1" : 0b1110111,
        "M-1" : 0b1110010,
        "D+M" : 0b1000010,
        "D-M" : 0b1010011,
        "M-D" : 0b1000111,
        "D&M" : 0b1000000,
        "D|M" : 0b1010101,  
        }

dest = {
        ""   : 0b000,
        "M"  : 0b001,
        "D"  : 0b010,
        "MD" : 0b011,
        "A"  : 0b100,
        "AM" : 0b101,
        "AD" : 0b110,
        "AMD": 0b111
        }

jump = {
        ""    : 0b000,
        "JGT" : 0b001,
        "JEQ" : 0b010,
        "JGE" : 0b011,
        "JLT" : 0b100,
        "JNE" : 0b101,
        "JLE" : 0b110,
        "JMP" : 0b111
        }

predefined = {
        "SP" : 0,
        "LCL" : 1,
        "ARG" : 2,
        "THIS" : 3,
        "THAT" : 4,
        "SCREEN" : 16384,
        "KBD" : 24576
        }

literals = {
 "R0": 0,
 "R1": 1,
 "R2": 2,
 "R3": 3,
 "R4": 4,
 "R5": 5,
 "R6": 6,
 "R7": 7,
 "R8": 8,
 "R9": 9,
 "R10": 10,
 "R11": 11,
 "R12": 12,
 "R13": 13,
 "R14": 14,
 "R15": 15,
 }

available_variable_address = 16

variables = {}

labels = {}

def read_asm(infile):
    with open(infile) as input_file:
        return input_file.readlines()
            
def clean_asm(asm_program):
    clean_asm = []
    for code_line in asm_program:
        stripped_line = code_line.strip()
        if stripped_line.startswith('//'):
            continue
        if not stripped_line:
            continue
        if stripped_line.find('//') != -1:
            stripped_line = stripped_line[:stripped_line.find('//')]
            stripped_line = stripped_line.rstrip()
        clean_asm.append(stripped_line)
    return clean_asm

class AInstruction:
    def CanHandle(self, code_line):
        return code_line.startswith('@')
    
    def parse(self, code_line):
        self.address = int(code_line[1:])
        
    def getBinary(self):
        return '0{:015b}'.format(self.address)
    
class CInstruction:
    def CanHandle(self, code_line):
        return not code_line.startswith('@')
    
    def parse(self, code_line):
        dest_pos = code_line.find('=')
        self.dest=""
        if dest_pos != -1:
            self.dest = code_line[0:dest_pos]
        
        jump_pos = code_line.find(';')
        self.comp=""
        self.jmp=""
        if jump_pos == -1 :
            self.comp = code_line[dest_pos+1:]
        else:
            self.comp = code_line[dest_pos+1:jump_pos]
            self.jmp = code_line[jump_pos+1:]
            
    
    def getBinary(self):
        return '111{:07b}{:03b}{:03b}'.format(
                comp[self.comp],
                dest[self.dest],
                jump[self.jmp]);
        
def parseLabels(asm_program):
    line_count = 0
    labeless_code = []
    for code_line in asm_program:
        if code_line.find('(') != -1:
            label = code_line[code_line.find('(')+1 : code_line.find(')')]
            labels[label] = line_count
        else:
            line_count+=1
            labeless_code.append(code_line)
    return labeless_code

def parseVariables(asm_program):
    global available_variable_address
    cleaned = []
    for code_line in asm_program:
        if not code_line.startswith('@'):
            cleaned.append(code_line)
        else:
            variable =  code_line[1:]
            if variable.isdigit():
                cleaned.append(code_line)
            else:
                if variable in literals:
                    cleaned.append('@' + str(literals[variable]))
                elif variable in labels:
                    cleaned.append('@' + str(labels[variable]))
                elif variable in variables:
                    cleaned.append('@' + str(variables[variable]))
                elif variable in predefined:
                    cleaned.append('@' + str(predefined[variable]))
                else:
                    cleaned.append('@' + str(available_variable_address))
                    variables[variable] = available_variable_address
                    available_variable_address +=1
    return cleaned
                    
def save_binary(outputfile, binary_code):
    with open(outputfile, 'w+') as dest:
        dest.writelines(binary_code)
        
def assemble(input_file, output_file):
    asm_prog = read_asm(input_file)
    asm_prog = clean_asm(asm_prog)
    asm_prog = parseLabels(asm_prog)
    asm_prog = parseVariables(asm_prog)
    binary_code = []
    aInstr = AInstruction()
    cInstr = CInstruction()
    for code_line in asm_prog:
        if code_line.startswith('@'):
            aInstr.parse(code_line)
            binary_code.append(aInstr.getBinary() + '\n')
        else:
            cInstr.parse(code_line)
            binary_code.append(cInstr.getBinary() + '\n')
    save_binary(output_file, binary_code)