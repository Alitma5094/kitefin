#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
import sys
from lex import Lexer
from parse import Parser
from asm import ASMGenerator
from codegen import ASMEmitter


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("filename")
    parser.add_argument(
        "--lex", action="store_true", help="run the lexer, but stop before parsing"
    )
    parser.add_argument(
        "--parse",
        action="store_true",
        help="run the lexer and parser, but stop before assembly generation",
    )
    parser.add_argument(
        "--codegen",
        action="store_true",
        help="perform lexing, parsing, and assembly generation, but stop before assembly generation",
    )
    parser.add_argument("-S", action="store_true")

    args = parser.parse_args()

    input_file = Path(args.filename)
    preprocessed_file = input_file.with_suffix(".i")

    subprocess.run(["cc", "-E", "-P", str(input_file), "-o", str(preprocessed_file)])

    with preprocessed_file.open() as f:
        lexer = Lexer(f.read())
        tokens = lexer.lex()
        # print(tokens)

    preprocessed_file.unlink()

    if args.lex:
        sys.exit()

    parser = Parser(tokens)
    tree = parser.parse()

    if args.parse:
        sys.exit()

    generator = ASMGenerator(tree)
    asm_tree = generator.generate()

    if args.codegen:
        sys.exit()

    emitter = ASMEmitter(asm_tree)
    assembly_file = input_file.with_suffix(".s")

    with assembly_file.open(mode="w") as f:
        f.write(emitter.emit())

    if args.S:
        sys.exit()

    subprocess.run(
        ["cc", str(assembly_file), "-o", str(input_file.with_suffix(""))], check=True
    )
    # assembly_file.unlink()


if __name__ == "__main__":
    main()
