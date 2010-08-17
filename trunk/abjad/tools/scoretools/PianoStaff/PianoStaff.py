from abjad.tools.scoretools.StaffGroup.StaffGroup import StaffGroup


class PianoStaff(StaffGroup):

   def __init__(self, music):
      StaffGroup.__init__(self, music)
      self.context = 'PianoStaff'
