from abjad.components.Staff import Staff


def make_rhythmic_staff(music):
   '''Make rhythmic staff.
   '''

   staff = Staff(music)
   staff.context = 'RhythmicStaff'
   
   return staff
