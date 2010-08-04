from abjad.components.Staff import Staff


def make_invisible_staff(music):
   '''Staff constructor that hides meter, bar line and staff lines.
   
   .. versionchanged:: 1.1.2
      Invisible staff class changed to invisible staff function.
   '''

   staff = Staff(music)
   staff.context = 'RhythmicStaff'
   staff.meter.transparent = True
   staff.bar_line.transparent = True
   staff.staff.transparent = True
   
   return staff
