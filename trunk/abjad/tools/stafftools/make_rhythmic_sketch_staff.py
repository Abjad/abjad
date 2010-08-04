from abjad.components.Staff import Staff


def make_rhythmic_sketch_staff(music):
   '''Make rhythmic staff with transparent meter and transparent bar lines.'''

   staff = Staff(music)
   staff.context = 'RhythmicStaff'
   staff.meter.transparent = True
   staff.bar_line.transparent = True

   return staff
