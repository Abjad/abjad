from abjad.staffgroup.staffgroup import StaffGroup


def GrandStaff(music):
   result = StaffGroup(music)
   result.context = 'GrandStaff'
   return result
