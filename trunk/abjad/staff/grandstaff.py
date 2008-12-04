from abjad.staff.staff import Staff


def GrandStaff(music):
   result = Staff(music)
   result.invocation.type = 'GrandStaff'
   result.brackets = 'simultaneous'
   return result
