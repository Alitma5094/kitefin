import platform
import parse
from dataclasses import dataclass
from abc import ABC

_bases, _dict = (ABC,), {}
Instruction = type("Instruction", _bases, _dict)
Operand = type("Operand", _bases, _dict)

@dataclass
class Imn(Operand):
    int: int

@dataclass
class Register(Operand):
    pass

@dataclass
class Mov(Instruction):
    src: Operand
    dst: Operand

@dataclass
class Ret(Instruction):
    pass

@dataclass
class Function:
    name: str
    instructions: list[Instruction]

@dataclass
class Program:
    function_definition: Function

class ASMGenerator:
    def __init__(self, tree: parse.Program):
        self.tree = tree

    def generate(self) -> Program:
        return self.convert_program(self.tree)

    def convert_program(self, programAST: parse.Program):
        function = self.convert_function(programAST.function_definition)
        return Program(function_definition=function)

    def convert_function(self, functionAST: parse.Function) -> Function:
        instructions = self.convert_return(functionAST.body)
        return Function(name=functionAST.name, instructions=instructions)

    def convert_return(self, returnAST: parse.Return) -> list[Instruction]:
        return_val = self.convert_constant(returnAST.exp)
        return [Mov(src=return_val, dst=Register()), Ret()]

    def convert_constant(self, constantAST: parse.Constant) -> Imn:
        return Imn(int=constantAST.val)

class ASMEmitter:
    def __init__(self, tree: Program):
        self.tree = tree
        self.P_IS_LINUX = platform.system() == "Linux"
        self.P_IS_MACOS = platform.system() == "Darwin"
    
    def emit(self) -> str:
        return self.emit_program(self.tree)

    def emit_program(self, program: Program) -> str:
        prog = self.emit_function(program.function_definition)
        if self.P_IS_LINUX:
            prog += '\t.section .node.GNU-stack."",@progbits'
        return prog

    def emit_function(self, function: Function) -> str:
        val = ""
        if self.P_IS_MACOS:
            val += f"\t.global _{function.name}\n_{function.name}:\n"
        else:
            val += f"\t.global {function.name}\n{function.name}:\n"

        for instr in function.instructions:
            val += self.emit_instruction(instr)
        
        return val
        
    def emit_instruction(self, instr: Instruction):
        match instr:
            case Mov():
                return f"\tmovl\t{self.emit_operand(instr.src)}, {self.emit_operand(instr.dst)}\n"
            case Ret():
                return "\tret\n"


    def emit_operand(self, op: Operand) -> str:
        match op:
            case Register():
                return "%eax"
            case Imn():
                return "$" + str(op.int)