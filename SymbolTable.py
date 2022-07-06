from symtable import Symbol


class SymbolTable:
  table = None

  def __init__(self):
    self.table = {}

  def enter_symbol(self, name, type):
    if name not in self.table:
      self.table[name] = type
    else:
      self.error()
  
  def has_key(self, name):
    return name in self.table

  def lookup_symbol(self, name):
    return self.table[name]

  def error(self):
    print("Semantic error: Duplicate declaration")
    exit()

  def __str__(self):
    ret = "{ "
    for name in self.table:
      ret += name + ": " + self.table[name] +", "
    return ret + "}"
