from abjad import *


def test_breaks_interface_alignment_offsets_01( ):
   '''NonMusicalPaperColumn alignment-offsets list.'''

   t = Score(Staff([Note(0, (1, 4))]) * 4)
   t[0].breaks.alignment_offsets = [0, -18, -54, -72]

   r'''
   \new Score <<
      \new Staff {
         \overrideProperty #"Score.NonMusicalPaperColumn"
         #'line-break-system-details
         #'((alignment-offsets . (0 -18 -54 -72)))
         c'4
      }
      \new Staff {
         c'4
      }
      \new Staff {
         c'4
      }
      \new Staff {
         c'4
      }
   >>
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Score <<\n\t\\new Staff {\n\t\t\\overrideProperty #"Score.NonMusicalPaperColumn"\n\t\t#\'line-break-system-details\n\t\t#\'((alignment-offsets . (0 -18 -54 -72)))\n\t\tc\'4\n\t}\n\t\\new Staff {\n\t\tc\'4\n\t}\n\t\\new Staff {\n\t\tc\'4\n\t}\n\t\\new Staff {\n\t\tc\'4\n\t}\n>>'
