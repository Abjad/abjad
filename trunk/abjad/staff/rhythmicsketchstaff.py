from abjad.staff.staff import Staff


def RhythmicSketchStaff(music):
   result = Staff(music)
   result.context = 'RhythmicStaff'
   result.meter.transparent = True
   result.barline.transparent = True
   return result
