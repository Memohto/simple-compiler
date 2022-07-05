# Imports
from Tokens import Tokens
from Stack import Stack

from Scanner import Scanner
from Parser import Parser

f = open("input.txt", "r")

stack = Stack(list(f.read()))

# Scanner
scanner = Scanner(stack)
tokens = scanner.scan_content()
print("Tokens: \n", tokens, "\n")

# Parser
parser = Parser(tokens)
tree = parser.parse_tokens()
print("Tree: \n", tree, "\n")

f.close()
  