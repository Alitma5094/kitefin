from dataclasses import dataclass
from lex import Token, TokenType


class Visitor:
    def visit_program(self, node):
        pass

    def visit_function(self, node):
        pass

    def visit_return(self, node):
        pass

    def visit_constant(self, node):
        pass


class Node:
    def accept(self, visitor):
        raise NotImplementedError()


@dataclass
class Constant(Node):
    val: int

    def accept(self, visitor):
        return visitor.visit_constant(self)


@dataclass
class Return(Node):
    exp: Constant

    def accept(self, visitor):
        return visitor.visit_return(self)


@dataclass
class Function(Node):
    name: str
    body: Return

    def accept(self, visitor):
        return visitor.visit_function(self)


@dataclass
class Program(Node):
    function_definition: Function

    def accept(self, visitor):
        return visitor.visit_program(self)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.index = 0

    def is_at_end(self) -> bool:
        return self.index >= len(self.tokens)

    def expect(self, expected: TokenType) -> Token:
        if self.is_at_end():
            raise RuntimeError("unexpected end of tokens")
        next_token = self.tokens[self.index]
        self.index += 1
        if not expected == next_token.token_type:
            raise RuntimeError(
                f"unexpected token: wanted {expected}, got {next_token.token_type}"
            )

        return next_token

    def parse(self) -> Program:
        program = self.parse_program()
        if not self.is_at_end():
            raise RuntimeError("tokens outside of function")
        return program

    def parse_program(self) -> Program:
        function = self.parse_function()
        return Program(function_definition=function)

    def parse_function(self) -> Function:
        self.expect(TokenType.KW_INT)
        identifier = self.parse_identifier()
        self.expect(TokenType.OPEN_PAREN)
        self.expect(TokenType.KW_VOID)
        self.expect(TokenType.CLOSE_PAREN)
        self.expect(TokenType.OPEN_BRACE)
        statement = self.parse_statement()
        self.expect(TokenType.CLOSE_BRACE)
        return Function(name=identifier, body=statement)

    def parse_statement(self) -> Return:
        self.expect(TokenType.KW_RETURN)
        return_val = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return Return(exp=return_val)

    def parse_expression(self) -> Constant:
        val = self.parse_int()
        return Constant(val=val)

    def parse_identifier(self) -> str:
        token = self.expect(TokenType.IDENTIFIER)
        return token.value

    def parse_int(self) -> int:
        token = self.expect(TokenType.CONSTANT)
        return int(token.value)
