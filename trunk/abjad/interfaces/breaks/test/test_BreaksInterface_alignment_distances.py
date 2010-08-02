from abjad import *


def test_BreaksInterface_alignment_distances_01( ):
   '''NonMusicalPaperColumn alignment-distances list.'''

   t = Score(Staff([Note(0, (1, 4))]) * 4)
   t[0].breaks.alignment_distances = [18, 18, 18]

   r'''
   \new Score <<
      \new Staff {
         \overrideProperty #"Score.NonMusicalPaperColumn"
         #'line-break-system-details
         #'((alignment-distances . (18 18 18)))
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
   assert t.format == '\\new Score <<\n\t\\new Staff {\n\t\t\\overrideProperty #"Score.NonMusicalPaperColumn"\n\t\t#\'line-break-system-details\n\t\t#\'((alignment-distances . (18 18 18)))\n\t\tc\'4\n\t}\n\t\\new Staff {\n\t\tc\'4\n\t}\n\t\\new Staff {\n\t\tc\'4\n\t}\n\t\\new Staff {\n\t\tc\'4\n\t}\n>>'
