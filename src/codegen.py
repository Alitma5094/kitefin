import platform

from asm import AsmVisitor


class ASMEmitter(AsmVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.P_IS_LINUX = platform.system() == "Linux"
        self.P_IS_MACOS = platform.system() == "Darwin"
        self.output = ""

    def emit(self):
        self.tree.accept(self)
        if self.P_IS_LINUX:
            self.output += '\t.section .note.GNU-stack,"",@progbits\n'
        return self.output

    def visit_program(self, node):
        node.function_definition.accept(self)

    def visit_function(self, node):
        if self.P_IS_MACOS:
            self.output += f"\t.global _{node.name}\n_{node.name}:\n"
        else:
            self.output += f"\t.global {node.name}\n{node.name}:\n"

        for instr in node.instructions:
            instr.accept(self)

    def visit_mov(self, node):
        src = node.src.accept(self)
        dst = node.dst.accept(self)
        self.output += f"\tmovl\t{src}, {dst}\n"

    def visit_ret(self, node):
        self.output += "\tret\n"

    def visit_imn(self, node):
        return f"${node.int}"

    def visit_register(self, node):
        return "%eax"
