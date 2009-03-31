from abjad.staff.staff import Staff


def RhythmicStaff(music):
   result = Staff(music)
   result.context = 'RhythmicStaff'
   return result
