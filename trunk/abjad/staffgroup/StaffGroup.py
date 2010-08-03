from abjad.context import _Context


class StaffGroup(_Context):

   def __init__(self, music = [ ]):
      _Context.__init__(self, music)
      self.parallel = True
      self.context = 'StaffGroup'
