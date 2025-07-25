from dataclasses import dataclass
from lex import Token, TokenType


@dataclass
class Constant:
    val: int

@dataclass
class Return:
    exp: Constant

@dataclass
class Function:
    name: str # Identifier
    body: Return # Statement

@dataclass
class Program:
    function_definition: Function


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
            raise RuntimeError(f"unexpected token: wanted {expected}, got {next_token.token_type}")
        
        return next_token
    
    def parse(self) -> Program:
        program = self.parseProgram()
        if not self.is_at_end():
            raise RuntimeError("tokens outside of function")
        return program

    def parseProgram(self) -> Program:
        function = self.parseFunction()
        return Program(function_definition=function)

    def parseFunction(self) -> Function:
        self.expect(TokenType.KW_INT)
        identifier = self.parseIdentifier()
        self.expect(TokenType.OPEN_PAREN)
        self.expect(TokenType.KW_VOID)
        self.expect(TokenType.CLOSE_PAREN)
        self.expect(TokenType.OPEN_BRACE)
        statement = self.parseStatement()
        self.expect(TokenType.CLOSE_BRACE)
        return Function(name=identifier, body=statement)

    def parseStatement(self) -> Return:
        self.expect(TokenType.KW_RETURN)
        return_val = self.parseExpression()
        self.expect(TokenType.SEMICOLON)
        return Return(exp=return_val)

    def parseExpression(self) -> Constant:
        val = self.parseInt()
        return Constant(val=val)


    def parseIdentifier(self) -> str:
        token = self.expect(TokenType.IDENTIFIER)
        return token.value

    def parseInt(self) -> int:
        token = self.expect(TokenType.CONSTANT)
        return int(token.value)
