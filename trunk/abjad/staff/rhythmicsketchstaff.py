from abjad.staff.staff import Staff


def RhythmicSketchStaff(music):
   result = Staff(music)
   result.invocation.type = 'RhythmicStaff'
   result.meter.transparent = True
   result.barline.transparent = True
   return result
