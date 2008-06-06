from container import Container

class Sequential(Container):

   def __init__(self, music = None):
      music = music or [ ]
      Container.__init__(self, music)
      self.brackets = 'curly'
