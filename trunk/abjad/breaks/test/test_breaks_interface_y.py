from abjad import *


def test_breaks_interface_y_01( ):
   '''``_BreaksInterface.y`` formats the \
   LilyPond ``NonMusicalPaperColumn`` prob.'''

   t = RigidMeasure((4, 8), construct.scale(4))
   t.breaks.line = True
   t.breaks.y = 80

   r'''
   {
           \overrideProperty #"Score.NonMusicalPaperColumn"
           #'line-break-system-details
           #'((Y-offset . 80))
           \time 4/8
           c'8
           d'8
           e'8
           f'8
           \break
   }
   '''

   assert t.format == '{\n\t\\overrideProperty #"Score.NonMusicalPaperColumn"\n\t#\'line-break-system-details\n\t#\'((Y-offset . 80))\n\t\\time 4/8\n\tc\'8\n\td\'8\n\te\'8\n\tf\'8\n\t\\break\n}'
