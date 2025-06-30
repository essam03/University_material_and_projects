#!/usr/bin/env python3
"""
Full-featured decompiler from assembly to C code
Supports: x86, x86_64, ARM, MIPS architectures
"""

import re
import sys
import os
import argparse
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set

# Supported binary and text extensions
BINARY_EXTENSIONS = {'.exe', '.dll', '.so', '.bin', '.elf', '.o', '.out', '.obj', '.ko', '.a', '.lib'}
TEXT_EXTENSIONS = {'.asm', '.s', '.S'}

class Decompiler:
    def _init_(self):
        self.arch = None
        self.bitness = 32  # Default to 32-bit
        self.labels = {}
        self.functions = {}
        self.data_sections = {}
        self.current_function = None
        self.variables = defaultdict(dict)
        self.control_flow = defaultdict(list)
        self.used_registers = set()
        self.stack_frame = {}
        self.string_literals = {}
        self.comments = {}
        self.analysis_complete = False

    def detect_architecture(self, lines: List[str]) -> str:
        """
        Detect assembly architecture from common directives
        """
        arch_patterns = {
            'x86': re.compile(r'\.(486|586|686|code32|intel_syntax)'),
            'x86_64': re.compile(r'\.(code64|x86_64|amd64)'),
            'arm': re.compile(r'\.(arm|thumb|arch\s+arm)'),
            'mips': re.compile(r'\.(mips|set\s+mips)')
        }
        
        for line in lines:
            for arch, pattern in arch_patterns.items():
                if pattern.search(line.lower()):
                    return arch
        
        # Fallback to instruction patterns
        x86_instructions = {'mov', 'push', 'pop', 'call', 'ret', 'int'}
        arm_instructions = {'ldr', 'str', 'bx', 'bl', 'stmfd', 'ldmfd'}
        mips_instructions = {'lw', 'sw', 'jr', 'jal', 'addiu'}
        
        for line in lines:
            if any(inst in line.lower() for inst in x86_instructions):
                return 'x86'
            if any(inst in line.lower() for inst in arm_instructions):
                return 'arm'
            if any(inst in line.lower() for inst in mips_instructions):
                return 'mips'
        
        return 'unknown'

    def parse_assembly(self, lines: List[str]) -> None:
        """
        Parse assembly code into structured format
        """
        self.arch = self.detect_architecture(lines)
        
        current_section = None
        current_function = None
        instruction_list = []
        
        for line_num, line in enumerate(lines):
            # Remove comments
            clean_line = re.sub(r';.*$', '', line).strip()
            if not clean_line:
                continue
                
            # Handle directives and sections
            if clean_line.startswith('.'):
                if clean_line.startswith(('.text', '.code')):
                    current_section = 'text'
                elif clean_line.startswith(('.data', '.rodata', '.bss')):
                    current_section = 'data'
                elif clean_line.startswith('.section'):
                    current_section = clean_line.split()[1]
                continue
                
            # Handle labels
            if clean_line.endswith(':'):
                label = clean_line[:-1]
                if current_section == 'text':
                    if current_function is not None:
                        self.functions[current_function]['instructions'] = instruction_list
                        instruction_list = []
                    current_function = label
                    self.functions[current_function] = {
                        'start': line_num,
                        'instructions': [],
                        'calls': set(),
                        'called_by': set()
                    }
                else:
                    self.labels[label] = {'type': 'data', 'value': None}
                continue
                
            # Handle instructions
            if current_function and current_section == 'text':
                instruction = self.normalize_instruction(clean_line)
                if instruction:
                    instruction_list.append(instruction)
                    # Detect function calls
                    if self.is_call_instruction(instruction):
                        target = self.extract_call_target(instruction)
                        if target:
                            self.functions[current_function]['calls'].add(target)
                            if target in self.functions:
                                self.functions[target]['called_by'].add(current_function)
        
        # Add last function's instructions
        if current_function and instruction_list:
            self.functions[current_function]['instructions'] = instruction_list

    def normalize_instruction(self, instruction: str) -> str:
        """
        Normalize instruction format for easier processing
        """
        # Remove redundant whitespace
        instruction = ' '.join(instruction.split())
        
        # Standardize instruction case
        parts = instruction.split()
        if parts:
            parts[0] = parts[0].lower()
            instruction = ' '.join(parts)
        
        return instruction

    def is_call_instruction(self, instruction: str) -> bool:
        """
        Check if instruction is a function call
        """
        if self.arch in ('x86', 'x86_64'):
            return instruction.startswith('call ')
        elif self.arch == 'arm':
            return instruction.startswith('bl ') or instruction.startswith('blx ')
        elif self.arch == 'mips':
            return instruction.startswith('jal ') or instruction.startswith('jalr ')
        return False

    def extract_call_target(self, instruction: str) -> Optional[str]:
        """
        Extract the target of a call instruction
        """
        if self.arch in ('x86', 'x86_64'):
            return instruction[5:].strip()
        elif self.arch == 'arm':
            return instruction[3:].strip()
        elif self.arch == 'mips':
            return instruction[4:].strip()
        return None

    def analyze_control_flow(self) -> None:
        """
        Analyze control flow within functions
        """
        for func_name, func_data in self.functions.items():
            instructions = func_data['instructions']
            blocks = []
            current_block = []
            branch_targets = set()
            
            # First pass to find all branch targets
            for i, inst in enumerate(instructions):
                if self.is_branch_instruction(inst):
                    target = self.extract_branch_target(inst)
                    if target:
                        branch_targets.add(target)
            
            # Second pass to split into basic blocks
            for i, inst in enumerate(instructions):
                # Start new block if this is a branch target
                if f'{func_name}:{i}' in branch_targets and current_block:
                    blocks.append(current_block)
                    current_block = []
                
                current_block.append(inst)
                
                # End block at branch instructions
                if self.is_branch_instruction(inst) and not self.is_call_instruction(inst):
                    blocks.append(current_block)
                    current_block = []
            
            if current_block:
                blocks.append(current_block)
            
            self.control_flow[func_name] = blocks

    def is_branch_instruction(self, instruction: str) -> bool:
        """
        Check if instruction is a branch/jump
        """
        if self.arch in ('x86', 'x86_64'):
            return (instruction.startswith(('jmp ', 'je ', 'jne ', 'jg ', 'jge ', 'jl ', 'jle ', 'ja ', 'jae ', 'jb ', 'jbe ')) or
                    instruction.startswith(('jz ', 'jnz ', 'jo ', 'jno ', 'js ', 'jns ', 'jp ', 'jnp ')))
        elif self.arch == 'arm':
            return instruction.startswith(('b ', 'beq ', 'bne ', 'bgt ', 'bge ', 'blt ', 'ble ', 'bal ', 'bx '))
        elif self.arch == 'mips':
            return instruction.startswith(('j ', 'jr ', 'beq ', 'bne ', 'bgtz ', 'blez ', 'bltz ', 'bgez '))
        return False

    def extract_branch_target(self, instruction: str) -> Optional[str]:
        """
        Extract branch target label
        """
        if self.arch in ('x86', 'x86_64'):
            if instruction.startswith('j'):
                return instruction.split()[1]
        elif self.arch == 'arm':
            if instruction.startswith('b'):
                return instruction.split()[1]
        elif self.arch == 'mips':
            if instruction.startswith(('j ', 'jr ', 'b')):
                return instruction.split()[1]
        return None

    def analyze_stack_usage(self) -> None:
        """
        Analyze stack usage in functions
        """
        for func_name, func_data in self.functions.items():
            stack_frame = {
                'size': 0,
                'variables': {},
                'parameters': {}
            }
            
            if self.arch in ('x86', 'x86_64'):
                self.analyze_x86_stack(func_name, stack_frame)
            elif self.arch == 'arm':
                self.analyze_arm_stack(func_name, stack_frame)
            elif self.arch == 'mips':
                self.analyze_mips_stack(func_name, stack_frame)
            
            self.stack_frame[func_name] = stack_frame

    def analyze_x86_stack(self, func_name: str, stack_frame: Dict) -> None:
        """
        Analyze stack usage for x86 architecture
        """
        instructions = self.functions[func_name]['instructions']
        stack_ptr = 0
        register_size = 4 if self.bitness == 32 else 8
        
        for inst in instructions:
            if inst.startswith('push'):
                stack_ptr += register_size
                reg = inst[5:].strip()
                stack_frame['variables'][f'var_{stack_ptr}'] = {
                    'offset': -stack_ptr,
                    'size': register_size,
                    'type': 'register',
                    'register': reg
                }
            elif inst.startswith('pop'):
                stack_ptr -= register_size
            elif inst.startswith('sub ') and 'esp' in inst:
                # Stack allocation
                parts = inst.split()
                if parts[1] == 'esp' and parts[2].startswith('0x'):
                    alloc_size = int(parts[2], 16)
                    stack_ptr += alloc_size
                    stack_frame['size'] = max(stack_frame['size'], stack_ptr)
            elif inst.startswith('mov ') and 'dword ptr [ebp-' in inst:
                # Local variable access
                match = re.search(r'\[ebp-0x([0-9a-f]+)\]', inst)
                if match:
                    offset = int(match.group(1), 16)
                    var_name = f'var_{offset}'
                    if var_name not in stack_frame['variables']:
                        stack_frame['variables'][var_name] = {
                            'offset': -offset,
                            'size': 4,
                            'type': 'local'
                        }
                    stack_frame['size'] = max(stack_frame['size'], offset)

    def analyze_arm_stack(self, func_name: str, stack_frame: Dict) -> None:
        """
        Analyze stack usage for ARM architecture
        """
        instructions = self.functions[func_name]['instructions']
        stack_ptr = 0
        
        for inst in instructions:
            if inst.startswith('push') or inst.startswith('stmfd sp!'):
                # Push multiple registers
                reg_list = inst[inst.find('{')+1:inst.find('}')].split(',')
                stack_ptr += 4 * len(reg_list)
                for reg in reg_list:
                    reg = reg.strip()
                    stack_frame['variables'][f'var_{stack_ptr}'] = {
                        'offset': -stack_ptr,
                        'size': 4,
                        'type': 'register',
                        'register': reg
                    }
            elif inst.startswith('sub sp, sp, #'):
                # Stack allocation
                alloc_size = int(inst[13:], 16)
                stack_ptr += alloc_size
                stack_frame['size'] = max(stack_frame['size'], stack_ptr)

    def analyze_mips_stack(self, func_name: str, stack_frame: Dict) -> None:
        """
        Analyze stack usage for MIPS architecture
        """
        instructions = self.functions[func_name]['instructions']
        stack_ptr = 0
        
        for inst in instructions:
            if inst.startswith('addiu $sp, $sp, -'):
                # Stack allocation
                alloc_size = int(inst[17:], 16)
                stack_ptr += alloc_size
                stack_frame['size'] = max(stack_frame['size'], stack_ptr)
            elif '($sp)' in inst:
                # Stack access
                match = re.search(r'(-?0x[0-9a-f]+)\($sp\)', inst)
                if match:
                    offset = int(match.group(1), 16)
                    var_name = f'var_{abs(offset)}'
                    if var_name not in stack_frame['variables']:
                        stack_frame['variables'][var_name] = {
                            'offset': offset,
                            'size': 4,
                            'type': 'local'
                        }

    def analyze_data_references(self) -> None:
        """
        Analyze references to data sections
        """
        for func_name, func_data in self.functions.items():
            instructions = func_data['instructions']
            
            for inst in instructions:
                if self.arch in ('x86', 'x86_64'):
                    if 'dword ptr [' in inst and ']' in inst:
                        # Memory access
                        mem_ref = inst[inst.find('[')+1:inst.find(']')]
                        if mem_ref in self.labels:
                            self.labels[mem_ref]['referenced_by'].append(func_name)
                elif self.arch == 'arm':
                    if '[' in inst and ']' in inst:
                        mem_ref = inst[inst.find('[')+1:inst.find(']')]
                        if mem_ref in self.labels:
                            self.labels[mem_ref]['referenced_by'].append(func_name)
                elif self.arch == 'mips':
                    if '(' in inst and ')' in inst:
                        mem_ref = inst[inst.find('(')+1:inst.find(')')]
                        if mem_ref in self.labels:
                            self.labels[mem_ref]['referenced_by'].append(func_name)

    def reconstruct_high_level_control_flow(self) -> Dict:
        """
        Reconstruct high-level control flow structures (if/else, loops)
        """
        control_structures = {}
        
        for func_name, blocks in self.control_flow.items():
            structures = []
            block_graph = self.build_block_graph(func_name, blocks)
            visited = set()
            
            # Identify loops
            loops = self.find_loops(block_graph)
            for loop in loops:
                structures.append({
                    'type': 'loop',
                    'entry': loop['entry'],
                    'body': loop['body'],
                    'exit': loop['exit']
                })
                visited.update(loop['body'])
            
            # Identify if-else structures
            for i, block in enumerate(blocks):
                if i in visited:
                    continue
                
                if len(block) > 0 and self.is_branch_instruction(block[-1]):
                    branch_target = self.extract_branch_target(block[-1])
                    if branch_target and branch_target in self.labels:
                        target_block = self.find_block_containing_label(blocks, branch_target)
                        if target_block is not None:
                            structures.append({
                                'type': 'if',
                                'condition_block': i,
                                'then_block': target_block,
                                'else_block': i + 1 if i + 1 < len(blocks) else None
                            })
                            visited.add(i)
                            visited.add(target_block)
                            if i + 1 < len(blocks):
                                visited.add(i + 1)
            
            control_structures[func_name] = structures
        
        return control_structures

    def build_block_graph(self, func_name: str, blocks: List[List[str]]) -> Dict[int, List[int]]:
        """
        Build control flow graph between basic blocks
        """
        graph = defaultdict(list)
        
        for i, block in enumerate(blocks):
            if not block:
                continue
                
            last_inst = block[-1]
            
            if self.is_branch_instruction(last_inst) and not self.is_call_instruction(last_inst):
                # Conditional or unconditional branch
                target = self.extract_branch_target(last_inst)
                if target and target in self.labels:
                    target_block = self.find_block_containing_label(blocks, target)
                    if target_block is not None:
                        graph[i].append(target_block)
                
                # Fall-through for conditional branches
                if not last_inst.startswith(('jmp', 'b ', 'bal ', 'j ')) and i + 1 < len(blocks):
                    graph[i].append(i + 1)
            elif not (self.is_call_instruction(last_inst) or last_inst.startswith(('ret', 'bx lr'))):
                # Fall-through
                if i + 1 < len(blocks):
                    graph[i].append(i + 1)
        
        return graph

    def find_loops(self, graph: Dict[int, List[int]]) -> List[Dict]:
        """
        Find loops in the control flow graph
        """
        loops = []
        visited = set()
        stack = []
        
        def dfs(node):
            nonlocal loops
            if node in visited:
                if node in stack:
                    # Found a loop
                    loop_start = stack.index(node)
                    loop_body = stack[loop_start:]
                    entry = loop_body[0]
                    exit_nodes = [succ for succ in graph[node] if succ not in loop_body]
                    
                    if exit_nodes:
                        loops.append({
                            'entry': entry,
                            'body': loop_body,
                            'exit': exit_nodes[0]
                        })
                return
            
            visited.add(node)
            stack.append(node)
            
            for neighbor in graph.get(node, []):
                dfs(neighbor)
            
            stack.pop()
        
        for node in graph:
            if node not in visited:
                dfs(node)
        
        return loops

    def find_block_containing_label(self, blocks: List[List[str]], label: str) -> Optional[int]:
        """
        Find the basic block that starts with the given label
        """
        for i, block in enumerate(blocks):
            if block and block[0].startswith(label + ':'):
                return i
        return None

    def reconstruct_variable_types(self) -> None:
        """
        Attempt to reconstruct variable types based on usage
        """
        for func_name, func_data in self.functions.items():
            instructions = func_data['instructions']
            stack_vars = self.stack_frame.get(func_name, {}).get('variables', {})
            
            for var_name, var_info in stack_vars.items():
                # Analyze usage patterns to guess type
                access_size = var_info.get('size', 4)
                is_signed = False
                is_float = False
                
                for inst in instructions:
                    if self.arch in ('x86', 'x86_64'):
                        if f'[ebp-{var_info["offset"]}]' in inst:
                            if 'dword' in inst:
                                access_size = 4
                            elif 'word' in inst:
                                access_size = 2
                            elif 'byte' in inst:
                                access_size = 1
                            if 'movsx' in inst:
                                is_signed = True
                            if 'fld' in inst or 'fstp' in inst:
                                is_float = True
                    elif self.arch == 'arm':
                        if f'[sp, #{var_info["offset"]}]' in inst:
                            if 'ldr' in inst or 'str' in inst:
                                access_size = 4
                            elif 'ldrh' in inst or 'strh' in inst:
                                access_size = 2
                                is_signed = 'ldrsh' in inst
                            elif 'ldrb' in inst or 'strb' in inst:
                                access_size = 1
                                is_signed = 'ldrsb' in inst
                    elif self.arch == 'mips':
                        if f'{var_info["offset"]}($sp)' in inst:
                            if 'lw' in inst or 'sw' in inst:
                                access_size = 4
                            elif 'lh' in inst or 'sh' in inst:
                                access_size = 2
                                is_signed = 'lh' in inst
                            elif 'lb' in inst or 'sb' in inst:
                                access_size = 1
                                is_signed = 'lb' in inst
                
                # Determine C type
                c_type = 'int'
                if is_float:
                    c_type = 'float' if access_size <= 4 else 'double'
                else:
                    if access_size == 1:
                        c_type = 'char' if not is_signed else 'signed char'
                    elif access_size == 2:
                        c_type = 'short' if not is_signed else 'signed short'
                    elif access_size == 4:
                        c_type = 'int' if not is_signed else 'signed int'
                    elif access_size == 8:
                        c_type = 'long long' if not is_signed else 'signed long long'
                
                var_info['c_type'] = c_type

    def generate_c_code(self) -> str:
        """
        Generate C code from the analyzed assembly
        """
        if not self.analysis_complete:
            self.analyze_control_flow()
            self.analyze_stack_usage()
            self.analyze_data_references()
            self.reconstruct_high_level_control_flow()
            self.reconstruct_variable_types()
            self.analysis_complete = True
        
        output = []
        output.append("/* Decompiled C code from assembly */")
        output.append("#include <stdint.h>\n")
        
        # Output data sections
        if self.labels:
            output.append("/* Data sections */")
            for label, label_data in self.labels.items():
                if label_data.get('type') == 'data':
                    output.append(f"void* {label}; /* Data reference */")
            output.append("")
        
        # Output function prototypes
        output.append("/* Function prototypes */")
        for func_name in self.functions:
            return_type = "void"  # Default, will be updated if we can determine
            output.append(f"{return_type} {func_name}();")
        output.append("")
        
        # Output each function
        for func_name, func_data in self.functions.items():
            output.append(f"/* Function: {func_name} */")
            
            # Generate function signature
            stack_frame = self.stack_frame.get(func_name, {})
            params = []
            locals = []
            
            for var_name, var_info in stack_frame.get('variables', {}).items():
                if var_info.get('type') == 'parameter':
                    params.append(f"{var_info.get('c_type', 'int')} {var_name}")
                else:
                    locals.append(f"{var_info.get('c_type', 'int')} {var_name};")
            
            signature = f"void {func_name}({', '.join(params)})"
            output.append(signature + " {")
            
            # Output local variables
            if locals:
                output.append("    /* Local variables */")
                for local in locals:
                    output.append(f"    {local}")
                output.append("")
            
            # Generate control flow
            control_structures = self.reconstruct_high_level_control_flow().get(func_name, [])
            blocks = self.control_flow[func_name]
            visited_blocks = set()
            
            for structure in control_structures:
                if structure['type'] == 'if':
                    cond_block = blocks[structure['condition_block']]
                    then_block = blocks[structure['then_block']]
                    else_block = blocks[structure['else_block']] if structure['else_block'] is not None else None
                    
                    # Generate condition
                    cond_code = self.translate_condition(cond_block[-1])
                    output.append(f"    if ({cond_code}) {{")
                    
                    # Generate then block
                    for inst in then_block[:-1]:
                        c_line = self.instruction_to_c(inst, func_name)
                        if c_line:
                            output.append(f"        {c_line}")
                    
                    if else_block:
                        output.append("    } else {")
                        for inst in else_block[:-1]:
                            c_line = self.instruction_to_c(inst, func_name)
                            if c_line:
                                output.append(f"        {c_line}")
                    
                    output.append("    }")
                    visited_blocks.update({structure['condition_block'], structure['then_block']})
                    if else_block:
                        visited_blocks.add(structure['else_block'])
                
                elif structure['type'] == 'loop':
                    entry_block = blocks[structure['entry']]
                    body_blocks = [blocks[i] for i in structure['body']]
                    exit_block = structure['exit']
                    
                    # Determine loop type (while, for, do-while)
                    # Simple heuristic: if condition is at start -> while, at end -> do-while
                    first_body_inst = body_blocks[0][0] if body_blocks else ""
                    last_body_inst = body_blocks[-1][-1] if body_blocks else ""
                    
                    if self.is_branch_instruction(last_body_inst) and self.extract_branch_target(last_body_inst) == entry_block[0].split(':')[0]:
                        # do-while style loop
                        output.append("    do {")
                        for block in body_blocks:
                            for inst in block[:-1]:  # Skip the branch at end
                                c_line = self.instruction_to_c(inst, func_name)
                                if c_line:
                                    output.append(f"        {c_line}")
                        output.append("    } while (1); /* TODO: Add condition */")
                    else:
                        # while style loop
                        cond_code = self.translate_condition(entry_block[-1])
                        output.append(f"    while ({cond_code}) {{")
                        for block in body_blocks:
                            for inst in block:
                                c_line = self.instruction_to_c(inst, func_name)
                                if c_line:
                                    output.append(f"        {c_line}")
                        output.append("    }")
                    
                    visited_blocks.update(structure['body'])
                    visited_blocks.add(structure['entry'])
            
            # Generate remaining blocks not part of high-level structures
            for i, block in enumerate(blocks):
                if i in visited_blocks:
                    continue
                
                for inst in block:
                    c_line = self.instruction_to_c(inst, func_name)
                    if c_line:
                        output.append(f"    {c_line}")
            
            output.append("}\n")
        
        return '\n'.join(output)

    def translate_condition(self, branch_inst: str) -> str:
        """
        Translate branch instruction to C condition
        """
        if self.arch in ('x86', 'x86_64'):
            if branch_inst.startswith('je '):
                return "== 0"  # TODO: Get actual condition
            elif branch_inst.startswith('jne '):
                return "!= 0"
            elif branch_inst.startswith('jg '):
                return "> 0"
            elif branch_inst.startswith('jge '):
                return ">= 0"
            elif branch_inst.startswith('jl '):
                return "< 0"
            elif branch_inst.startswith('jle '):
                return "<= 0"
        elif self.arch == 'arm':
            if branch_inst.startswith('beq '):
                return "== 0"
            elif branch_inst.startswith('bne '):
                return "!= 0"
            elif branch_inst.startswith('bgt '):
                return "> 0"
            elif branch_inst.startswith('bge '):
                return ">= 0"
            elif branch_inst.startswith('blt '):
                return "< 0"
            elif branch_inst.startswith('ble '):
                return "<= 0"
        elif self.arch == 'mips':
            if branch_inst.startswith('beq '):
                return "== 0"
            elif branch_inst.startswith('bne '):
                return "!= 0"
            elif branch_inst.startswith('bgtz '):
                return "> 0"
            elif branch_inst.startswith('blez '):
                return "<= 0"
        
        return "1 /* Unknown condition */"

    def instruction_to_c(self, inst: str, func_name: str) -> Optional[str]:
        """
        Translate single assembly instruction to C statement
        """
        if not inst:
            return None
        
        # Handle function calls
        if self.is_call_instruction(inst):
            target = self.extract_call_target(inst)
            return f"{target}();"
        
        # Handle returns
        if inst in ('ret', 'bx lr'):
            return "return;"
        
        # Handle basic arithmetic
        if self.arch in ('x86', 'x86_64'):
            if inst.startswith('mov '):
                parts = inst.split()
                if len(parts) == 3:
                    return f"{parts[1]} = {parts[2]};"
            elif inst.startswith('add '):
                parts = inst.split()
                if len(parts) == 3:
                    return f"{parts[1]} += {parts[2]};"
            elif inst.startswith('sub '):
                parts = inst.split()
                if len(parts) == 3:
                    return f"{parts[1]} -= {parts[2]};"
        elif self.arch == 'arm':
            if inst.startswith('mov '):
                parts = inst.split()
                if len(parts) >= 3:
                    return f"{parts[1]} = {parts[2]};"
            elif inst.startswith('add '):
                parts = inst.split()
                if len(parts) >= 4:
                    return f"{parts[1]} = {parts[2]} + {parts[3]};"
            elif inst.startswith('sub '):
                parts = inst.split()
                if len(parts) >= 4:
                    return f"{parts[1]} = {parts[2]} - {parts[3]};"
        elif self.arch == 'mips':
            if inst.startswith('move '):
                parts = inst.split()
                if len(parts) == 3:
                    return f"{parts[1]} = {parts[2]};"
            elif inst.startswith('add '):
                parts = inst.split()
                if len(parts) == 4:
                    return f"{parts[1]} = {parts[2]} + {parts[3]};"
            elif inst.startswith('sub '):
                parts = inst.split()
                if len(parts) == 4:
                    return f"{parts[1]} = {parts[2]} - {parts[3]};"
        
        # Fallback - just comment the instruction
        return f"/* {inst} */"

def main():
    print("=== Advanced Assembly to C Decompiler ===")

    input_path = r"C:\Users\User\Downloads\disassembly_output1.asm"
    output_path = r"C:\Users\User\Downloads\result.c"

    # Check file extension
    _, ext = os.path.splitext(input_path)
    if ext.lower() not in TEXT_EXTENSIONS:
        print(f"Warning: Input file has extension {ext} which is not a recognized assembly extension")

    # Read input file
    try:
        with open(input_path, 'r') as f:
            lines = f.readlines()
    except IOError as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

    # Process assembly
    decompiler = Decompiler()
    decompiler.parse_assembly(lines)

    # Generate C code
    c_code = decompiler.generate_c_code()

    # Write output
    try:
        with open(output_path, 'w') as f:
            f.write(c_code)
        print(f"\n✅ Successfully decompiled to: {output_path}")
    except IOError as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)
