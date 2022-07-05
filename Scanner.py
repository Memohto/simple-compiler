from Tokens import Tokens


class Scanner:
  stack = None
  tokens = None

  def __init__(self, stack):
    self.stack = stack
    self.tokens = Tokens()

  def scan_content(self):
    while not self.stack.eof():
      self.scan_next()
    if not self.tokens.is_empty() and self.tokens.last() != "$":
      self.scan_next()
    return self.tokens

  def scan_next(self):
    token = {}
    while not self.stack.eof() and (self.stack.peek() == " " or self.stack.peek() == "\n"):
      self.stack.advance() 
    if self.stack.eof():
      token["type"] = "$"
    else:
      if self.stack.peek() in '1234567890':
        token = self.scan_digits()
      else:  
        char = self.stack.advance()
        if char in 'abcdeghjklmnoqrstuvwxyz':
          token["type"] = "id"
          token["val"] = char
        elif char == "f":
          token["type"] = "floatdcl"
        elif char == "i":
          token["type"] = "intdcl"
        elif char == "p":
          token["type"] = "print"
        elif char == "=":
          token["type"] = "assign"
        elif char == "+":
          token["type"] = "plus"
        elif char == "-":
          token["type"] = "minus"
        else:
          self.error()
    self.tokens.append(token)

  def scan_digits(self):
    token = {
      "type": "",
      "val": ""
    }
    while self.stack.peek() in "1234567890":
      token["val"] = token["val"] + self.stack.advance()
    if self.stack.peek() != ".":
      token["type"] = "inum"
    else:
      token["type"] = "fnum"
      token["val"] = token["val"] + self.stack.advance()
      while self.stack.peek() in "1234567890":
        token["val"] = token["val"] + self.stack.advance()
    return token
  
  def error(self):
    print("Lexical error")
    exit()
