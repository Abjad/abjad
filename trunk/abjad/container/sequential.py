from abjad.container.container import Container


class Sequential(Container):

   def __init__(self, music = None):
      music = music or [ ]
      Container.__init__(self, music)
      #self.brackets = 'curly'
      self.parallel = False

   ## OVERLOADS ##

   def __repr__(self):
      return 'Sequential(%s)' % self._summary
