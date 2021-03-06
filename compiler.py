# Imports
from Tokens import Tokens
from Stack import Stack
from SymbolTable import SymbolTable

from Scanner import Scanner
from Parser import Parser

# Input
f = open("input.txt", "r")
stack = Stack(list(f.read()))
f.close()

# Scanner
scanner = Scanner(stack)
tokens = scanner.scan_content()
print("Tokens: \n", tokens, "\n")

# Parser
parser = Parser(tokens)
tree = parser.parse_tokens()

# Symbol table
symbol_table = SymbolTable()
for child in tree.children:
  if child.type == 'floatdcl':
    symbol_table.enter_symbol(child.val, 'float')
  elif child.type == 'intdcl':
    symbol_table.enter_symbol(child.val, 'int')
print("Symbol table: \n", symbol_table, "\n")

# Type checking
tree.type_check(symbol_table)
print("Tree: \n", tree, "\n") 

# Code generation
instructions = tree.generate_code()

# Output
f = open("output.txt", "w")
for line in instructions:
  f.write(line+'\n')
f.close()
  