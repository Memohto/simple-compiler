class Stack:
  content = None

  def __init__(self, content = []):
    self.content = content
  
  def peek(self):
    return self.content[0]

  def advance(self):
    return self.content.pop(0)

  def eof(self):
    return len(self.content) == 0