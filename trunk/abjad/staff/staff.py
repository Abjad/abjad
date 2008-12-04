from abjad.context.context import _Context


class Staff(_Context):

   def __init__(self, music = None):
      music = music or [ ]
      _Context.__init__(self, music)
      self.invocation = 'Staff'
