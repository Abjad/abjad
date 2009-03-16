from abjad.staffgroup.staffgroup import StaffGroup


def GrandStaff(music):
   result = StaffGroup(music)
   result.invocation.type = 'GrandStaff'
   return result
