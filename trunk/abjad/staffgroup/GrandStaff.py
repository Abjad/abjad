from abjad.staffgroup.StaffGroup import StaffGroup


#def GrandStaff(music):
#   result = StaffGroup(music)
#   result.context = 'GrandStaff'
#   return result

class GrandStaff(StaffGroup):

   def __init__(self, music):
      StaffGroup.__init__(self, music)
      self.context = 'GrandStaff'
