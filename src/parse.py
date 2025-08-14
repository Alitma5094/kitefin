from abc import ABC
from dataclasses import dataclass
from enum import Enum
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

    def visit_unary(self, node):
        pass


class UnaryOp(Enum):
    NEGATE = 0
    COMPLEMENT = 1

    def from_token(token: Token) -> "UnaryOp":
        match token.token_type:
            case TokenType.TILDE:
                return UnaryOp.COMPLEMENT
            case TokenType.HYPHEN:
                return UnaryOp.NEGATE
            case _:
                raise RuntimeError(
                    f"unexpected token type: wanted 'TILDE | HYPHEN', got {token.token_type}"
                )


_bases, _dict = (ABC,), {}
Statement = type("Statement", _bases, _dict)
Expression = type("Expression", _bases, _dict)


class Node:
    def accept(self, visitor):
        raise NotImplementedError()


@dataclass
class Constant(Node, Expression):
    val: int

    def accept(self, visitor):
        return visitor.visit_constant(self)


@dataclass
class Unary(Node, Expression):
    unary_operator: UnaryOp
    exp: Expression

    def accept(self, visitor):
        return visitor.visit_unary(self)


@dataclass
class Return(Node, Statement):
    exp: Expression

    def accept(self, visitor):
        return visitor.visit_return(self)


@dataclass
class Function(Node):
    name: str
    body: Statement

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

    def peek(self) -> Token:
        return self.tokens[self.index]

    def consume(self) -> Token:
        next_token = self.tokens[self.index]
        self.index += 1
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

    def parse_statement(self) -> Statement:
        self.expect(TokenType.KW_RETURN)
        return_val = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return Return(exp=return_val)

    def parse_expression(self) -> Expression:
        next_token = self.peek()
        match next_token.token_type:
            case TokenType.CONSTANT:
                val = self.parse_int()
                return Constant(val=val)
            case TokenType.TILDE | TokenType.HYPHEN:
                self.consume()
                operator = UnaryOp.from_token(next_token)
                inner_exp = self.parse_expression()
                return Unary(unary_operator=operator, exp=inner_exp)
            case TokenType.OPEN_PAREN:
                self.expect(TokenType.OPEN_PAREN)
                inner_exp = self.parse_expression()
                self.expect(TokenType.CLOSE_PAREN)
                return inner_exp
            case _:
                raise RuntimeError("Malformed expression")

    def parse_identifier(self) -> str:
        token = self.expect(TokenType.IDENTIFIER)
        return token.value

    def parse_int(self) -> int:
        token = self.expect(TokenType.CONSTANT)
        return int(token.value)
