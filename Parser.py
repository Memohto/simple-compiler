from cmath import exp
from Node import Node

class Parser:
  tokens = None
  root = None

  def __init__(self, tokens):
    self.tokens = tokens
    self.root = Node()

  def parse_tokens(self):
    self.prog()
    return self.root

  def prog(self):
    self.root.set_info("PROG")
    self.root.add_childs(self.dcls())
    self.root.add_childs(self.stmts())
    
  def dcls(self):
    childs = []
    if self.tokens.peek() == "floatdcl" or self.tokens.peek() == "intdcl":
      childs += self.dcl()
      childs += self.dcls()
    return childs

  def dcl(self):
    type = ""
    val = ""
    current = self.tokens.peek()
    if current == "floatdcl" or current == "intdcl":
      type = self.tokens.match(current)["type"]
      val = self.tokens.match("id")["val"]
    else:
      self.error()
    return [Node(type, val)]

  def stmts(self):
    childs = []
    if self.tokens.peek() == "id" or self.tokens.peek() == "print":
      childs += self.stmt()
      childs += self.stmts()
    else:
      if self.tokens.peek() != "$":
        self.error()
    return childs

  def stmt(self):
    token = None
    node = Node()
    if self.tokens.peek() == "id":
      token = self.tokens.match("id")
      self.tokens.match("assign")
      node.set_info("assign")
      node.add_childs([Node(token["type"], token["val"])])
      val_node = self.val()
      node.add_childs(self.expr(val_node))
    else:
      if self.tokens.peek() == "print":
        self.tokens.match("print")
        token = self.tokens.match("id")
        node.set_info("print", token["val"])
      else:
        self.error()
    return [node]

  def expr(self, val_node):
    node = None
    current = self.tokens.peek()
    if current == "plus" or current == "minus": 
      node = Node(current)
      node.add_childs(val_node)
      self.tokens.match(current)
      next_val = self.val()
      node.add_childs(self.expr(next_val))
    if node is not None:
      return [node]
    return val_node

  def val(self):
    token = None
    current = self.tokens.peek()
    if current == "id" or current == "inum" or current == "fnum":
      token = self.tokens.match(current)
    else:
      self.error()
    return [Node(token["type"], token["val"])]

  def error(self):
    print("Parsing error")
    exit()