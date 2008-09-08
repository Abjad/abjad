from abjad.context.context import Context

class StaffGroup(Context):

   def __init__(self, music = [ ]):
      Context.__init__(self, music)
      self.brackets = 'double-angle'
      self.invocation = 'StaffGroup'
