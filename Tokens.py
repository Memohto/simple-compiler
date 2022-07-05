class Tokens:
  tokens = None

  def __init__(self):
    self.tokens = []

  def is_empty(self):
    return len(self.tokens) == 0
  
  def last(self):
    return self.tokens[len(self.tokens) - 1]["type"]
  
  def peek(self):
    return self.tokens[0]["type"]

  def match(self, simbol):
    token = self.tokens.pop(0)
    if token["type"] != simbol:
      print("Parsing error")
      exit()
    return token

  def append(self, token):
    self.tokens.append(token)

  def __str__(self):
    ret = ""
    for token in self.tokens:
      ret += token["type"]
      if "val" in token:
        ret += ": " + token["val"]
      ret += ", "
    return ret