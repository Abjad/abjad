from abjad.containers.container import Container


class Sequential(Container):

   def __init__(self, music = None):
      music = music or [ ]
      Container.__init__(self, music)
      self.brackets = 'curly'

   def __repr__(self):
      return 'Sequential(%s)' % self._summary
