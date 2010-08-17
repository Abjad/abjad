from abjad.tools.scoretools.StaffGroup.StaffGroup import StaffGroup


class GrandStaff(StaffGroup):

   def __init__(self, music):
      StaffGroup.__init__(self, music)
      self.context = 'GrandStaff'
