from abjad import *


def test_breaks_interface_x_01( ):
   '''
   _BreaksInterface x formats the LilyPond NonMusicalPaperColumn prob.
   '''

   t = RigidMeasure((4, 8), construct.scale(4))
   t[-1].breaks.line = True
   t[-1].breaks.x = 40

   r'''
      \time 4/8
      c'8
      d'8
      e'8
      f'8
      \break
      \overrideProperty #"Score.NonMusicalPaperColumn"
      #'line-break-system-details
      #'((X-offset . 40))
   '''

   assert t.format == '\t\\time 4/8\n\tc\'8\n\td\'8\n\te\'8\n\tf\'8\n\t\\break\n\t\\overrideProperty #"Score.NonMusicalPaperColumn"\n\t#\'line-break-system-details\n\t#\'((X-offset . 40))'

