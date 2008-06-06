from container import Container

class Parallel(Container):

   def __init__(self, music = None):
      music = music  or [ ]
      Container.__init__(self, music)
      self.brackets = 'double-angle'
