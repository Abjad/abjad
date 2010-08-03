from abjad.Staff.Staff import Staff


#def RhythmicStaff(music):
#   result = Staff(music)
#   result.context = 'RhythmicStaff'
#   return result

class RhythmicStaff(Staff):

   def __init__(self, music):
      Staff.__init__(self, music)
      self.context = 'RhythmicStaff'
