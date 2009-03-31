from abjad.context.context import _Context


class Voice(_Context):

   def __init__(self, music = None):
      music = music or [ ]
      _Context.__init__(self, music)
      self.context = 'Voice'
