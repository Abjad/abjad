from abjad.context.context import _Context


class StaffGroup(_Context):

   def __init__(self, music = [ ]):
      _Context.__init__(self, music)
      self.brackets = 'double-angle'
      self.invocation = 'StaffGroup'
