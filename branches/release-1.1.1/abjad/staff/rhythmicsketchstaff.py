from abjad.staff.staff import Staff


#def RhythmicSketchStaff(music):
#   result = Staff(music)
#   result.context = 'RhythmicStaff'
#   result.meter.transparent = True
#   result.barline.transparent = True
#   return result

class RhythmicSketchStaff(Staff):

   def __init__(self, music):
      Staff.__init__(self, music)
      self.context = 'RhythmicStaff'
      self.meter.transparent = True
      self.barline.transparent = True
