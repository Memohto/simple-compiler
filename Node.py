import copy

class Node:
  children = None

  def __init__(self, type = "", val = "", data_type = ""):
    self.type = type
    self.val = val
    self.data_type = data_type
    self.children = []

  def add_children(self, new_children):
    self.children += new_children

  def set_info(self, type = "", val = ""):
    self.type = type
    self.val = val

  def type_check(self, symbol_table):
    for child in self.children:
      child.type_check(symbol_table)
    if symbol_table.has_key(self.val):
      self.data_type = symbol_table.lookup_symbol(self.val)
    elif self.type == 'fnum':
      self.data_type = 'float'
    elif self.type == 'inum':
      self.data_type = 'int'
    elif self.type == 'plus' or self.type == 'minus':
      self.data_type = self.consistent(self.children[0], self.children[1])
    elif self.type == 'assign':
      self.data_type = self.convert(self.children[1], self.children[0].data_type)
      
  def generalize(self, type_1, type_2):
    type = ""
    if type_1 == 'float'  or type_2 == 'float':
      type = 'float'
    else:
      type = 'int'
    return type

  def consistent(self, node_1, node_2):
    type = self.generalize(node_1.data_type, node_2.data_type)
    self.convert(node_1, type)
    self.convert(node_2, type)
    return type

  def convert(self, node, type):
    if node.data_type == 'int' and type == 'float':
      temp_node = copy.deepcopy(node)

      node.type = "int2float"
      node.val = ""
      node.data_type = "float"
      node.children = []
      node.add_children([temp_node])
      return 'float'
    elif node.data_type == 'float' and type == 'int':
      self.error()
    return type

  def generate_code(self):
    instructions = []
    for child in self.children:
      _, _, new_instructions = child.generate_child_code()
      instructions += new_instructions
      
    return instructions

  def generate_child_code(self, reg_num = 0):
    register = 'r'+str(reg_num)
    current_num = reg_num
    instructions = []
    new_instructions = []

    if self.type in ['floatdcl', 'intdcl', 'print']:
      register = self.val
      instructions.append(self.type + ' ' + self.val)
      current_num -= 1
    elif self.type in ['fnum', 'inum', 'id']:
      register = self.val
      current_num -= 1
    elif self.type == 'int2float':
      register = 'r'+str(current_num)
      right_register, current_num, new_instructions = self.children[0].generate_child_code(current_num + 1)
      instructions.append(register + ' = ' + self.type + ' ' + right_register)
    elif self.type == 'plus' or self.type == 'minus':
      register = 'r'+str(current_num)
      left_register, current_num, left_instructions = self.children[0].generate_child_code(current_num + 1)
      right_register, current_num, right_instructions = self.children[1].generate_child_code(current_num + 1)
      new_instructions = new_instructions + left_instructions + right_instructions
      if self.type == 'plus':
        instructions.append(register + ' = ' + left_register + ' + ' + right_register)
      else:
        instructions.append(register + ' = ' + left_register + ' - ' + right_register)
    elif self.type == 'assign':
      prev_register, current_num, new_instructions = self.children[1].generate_child_code(current_num + 1)
      instructions.append(self.children[0].val + ' = ' + prev_register)
    
    return register, current_num, new_instructions + instructions
 
  def error(self):
    print("Semantic error: Illegal type conversion")
    exit()
    
  def __str__(self, level = 0):
    ret = "\t"*level+(self.type + ': ' + str(self.val) + ' (' + self.data_type + ')')+"\n"
    for child in self.children:
      ret += child.__str__(level+1)
    return ret