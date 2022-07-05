class Node:
  token = None
  childs = None

  def __init__(self, type = "", val = ""):
    self.type = type
    self.val = val
    self.childs = []

  def add_childs(self, new_childs):
    self.childs += new_childs

  def set_info(self, type = "", val = ""):
    self.type = type
    self.val = val
    
  def __str__(self, level = 0):
    ret = "\t"*level+(self.type + ': ' + str(self.val))+"\n"
    for child in self.childs:
      ret += child.__str__(level+1)
    return ret