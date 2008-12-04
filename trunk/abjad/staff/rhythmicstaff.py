from abjad.staff.staff import Staff


def RhythmicStaff(music):
   result = Staff(music)
   result.invocation.type = 'RhythmicStaff'
   return result
