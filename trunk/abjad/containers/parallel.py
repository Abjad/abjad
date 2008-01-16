from container import Container

class Parallel(Container):

   def __init__(self, music = [ ]):
      Container.__init__(self, music)
      self.brackets = 'double-angle'
