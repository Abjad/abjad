from abjad.staff.staff import Staff


def PianoStaff(music):
   result = Staff(music)
   result.invocation.type = 'PianoStaff'
   result.brackets = 'simultaneous'
   return result
