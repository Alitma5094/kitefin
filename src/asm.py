import parse
from dataclasses import dataclass
from abc import ABC


class AsmVisitor:
    def visit_program(self, node):
        pass

    def visit_function(self, node):
        pass

    def visit_mov(self, node):
        pass

    def visit_ret(self, node):
        pass

    def visit_imn(self, node):
        pass

    def visit_register(self, node):
        pass


class Node:
    def accept(self, visitor):
        raise NotImplementedError()


_bases, _dict = (ABC,), {}
Instruction = type("Instruction", _bases, _dict)
Operand = type("Operand", _bases, _dict)


@dataclass
class Imn(Operand, Node):
    int: int

    def accept(self, visitor):
        return visitor.visit_imn(self)


@dataclass
class Register(Operand, Node):
    def accept(self, visitor):
        return visitor.visit_register(self)


@dataclass
class Mov(Instruction, Node):
    src: Operand
    dst: Operand

    def accept(self, visitor):
        return visitor.visit_mov(self)


@dataclass
class Ret(Instruction, Node):
    def accept(self, visitor):
        return visitor.visit_ret(self)


@dataclass
class Function(Node):
    name: str
    instructions: list[Instruction]

    def accept(self, visitor):
        return visitor.visit_function(self)


@dataclass
class Program(Node):
    function_definition: Function

    def accept(self, visitor):
        return visitor.visit_program(self)


class ASMGenerator(parse.Visitor):
    def __init__(self, tree: Program):
        self.instructions = []
        self.function_name = None
        self.tree = tree

    def generate(self):
        return self.tree.accept(self)

    def visit_program(self, node: Program):
        function = node.function_definition.accept(self)
        return Program(function_definition=function)

    def visit_function(self, node: Function):
        self.instructions = []
        self.function_name = node.name
        body_instrs = node.body.accept(self)
        return Function(name=self.function_name, instructions=body_instrs)

    def visit_return(self, node: parse.Return):
        value = node.exp.accept(self)
        return [Mov(src=value, dst=Register()), Ret()]

    def visit_constant(self, node: parse.Constant):
        return Imn(int=node.val)
