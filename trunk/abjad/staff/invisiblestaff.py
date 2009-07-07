from abjad.staff.staff import Staff


def InvisibleStaff(music):
   '''.. versionadded:: 1.1.1 
   
   A Staff class that hides meter, barline and stafflines at 
   construction time.'''

   result = Staff(music)
   result.context = 'RhythmicStaff'
   result.meter.transparent = True
   result.barline.transparent = True
   result.staff.transparent = True
   return result
