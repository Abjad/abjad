from abjad.staff.staff import Staff


#def InvisibleStaff(music):
#   '''.. versionadded:: 1.1.1 
#   
#   A Staff class that hides meter, bar_line and stafflines at 
#   construction time.'''
#
#   result = Staff(music)
#   result.context = 'RhythmicStaff'
#   result.meter.transparent = True
#   result.bar_line.transparent = True
#   result.staff.transparent = True
#   return result

class InvisibleStaff(Staff):
   '''.. versionadded:: 1.1.1 
   
   A Staff class that hides meter, bar_line and stafflines at 
   construction time.'''

   def __init__(self, music):
      Staff.__init__(self, music)
      self.context = 'RhythmicStaff'
      self.meter.transparent = True
      self.bar_line.transparent = True
      self.staff.transparent = True
