"""
pass in a text file with MIPS style assembly
usage:
python mcassembler.py [filename]
"""

import sys
import os

opcodes = {'zero':'000',
    'clr':'000',
    'and':'000',
    'nand':'000',
    'xor':'000',
    'xnor':'000',
    'or':'000',
    'nor':'000',
    'add':'000',
    'addi':'001',
    'move':'010',
    'not':'011',
    'jeq':'100',
    'jneq':'100',
    'sb':'101',
    'lb':'110',
    'sw':'101',
    'lw':'110',
    'dr':'111'}

functs = {'zero':'0000',
    'clr':'0000',
    'and':'0010',
    'nand':'0011',
    'xor':'0100',
    'xnor':'0101',
    'or':'0110',
    'nor':'0111',
    'add':'1000',
    'jeq':'0',
    'jneq':'1'}

regnums = {'$r0':'0', '$r1':'1', 'r0':'0', 'r1':'1'}

filename = sys.argv[1]

if filename not in os.listdir():
    print("File not found.")
else:
    lines = open(filename).read().split('\n')

    for i in range(0, len(lines)):
        if '#' in lines[i]:
            lines[i] = lines[i][:lines[i].index('#')].strip()

    print('\n'.join(lines))
    print()

    bin_instructions = []

    for i in range(0, len(lines)):
        bin_instr = ''
        try:
            line = lines[i]
            opstr = line.split(' ')[0]
            opcode = opcodes[opstr]

            bin_instr += opcode

            args = line.split(' ', 1)[1].split(', ')

            if len(args) == 1:
                # jumping
                if opstr in ['jeq', 'jneq']:
                    bin_instr += functs[opstr]
                    
                    # 4-bit immediate
                    if int(args[0]) < 16:
                        bin_instr += format(int(args[0]), '04b')
                    else:
                        raise Exception('Immediate is too large.')
                # commutative operations
                else:
                    bin_instr += regnums[args[0]]
                    if opstr in functs:
                        bin_instr += functs[opstr]
                    else:
                        bin_instr += '0000'
            elif len(args) == 2:
                # two register arguments
                if opstr in ['move', 'not']:
                    bin_instr += regnums[args[0]]
                    bin_instr += regnums[args[1]]
                    bin_instr += '000'
                # register and immediate arguments
                elif opstr in ['sb', 'lb']:
                    bin_instr += regnums[args[0]]

                    # 4-bit immediate
                    if int(args[1]) < 16:
                        bin_instr += format(int(args[1]), '04b')
                    else:
                        raise Exception('Immediate is too large.')
                # something else
                else:
                    raise Exception('Unrecognized opcode with 2 arguments.')
            elif len(args) == 3:
                bin_instr += regnums[args[0]]
                # addi
                if opstr in ['addi']:
                    bin_instr += regnums[args[1]]
                    if int(args[2]) < 8:
                        bin_instr += format(int(args[2]), '03b')
                    else:
                        raise Exception('Immediate is too large.')
            
            bin_instructions.append(bin_instr)
        except Exception as e:
            print(f'Failed to parse line {i}.\n{e}')
        
    for i in range(0, len(bin_instructions)):
        bin_instructions[i] = bin_instructions[i][:4] + ' ' + bin_instructions[i][4:]
    print('\n'.join(bin_instructions))