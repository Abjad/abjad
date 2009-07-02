from abjad import *


def test_anonymous_measure_meter_change_01( ):
   '''Meter sequence: 1/4, 3/8, 1/4.
   Important that last measure format *only* meter 1/4.
   If last measure formats *both* meter 1/4 and meter 3/8, there's contention.
   Contention between leaf and measure as to who should format meter.'''

   t = Staff([ ])
   t.append(AnonymousMeasure(construct.scale(2)))
   t.append(AnonymousMeasure(construct.scale(3)))
   t.append(AnonymousMeasure(construct.scale(2)))

   r'''
   \new Staff {
           {
                   \override Staff.TimeSignature #'stencil = ##f
                   \time 1/4
                   c'8
                   d'8
                   \revert Staff.TimeSignature #'stencil
           }
           {
                   \override Staff.TimeSignature #'stencil = ##f
                   \time 3/8
                   c'8
                   d'8
                   e'8
                   \revert Staff.TimeSignature #'stencil
           }
           {
                   \override Staff.TimeSignature #'stencil = ##f
                   \time 1/4
                   c'8
                   d'8
                   \revert Staff.TimeSignature #'stencil
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\override Staff.TimeSignature #'stencil = ##f\n\t\t\\time 1/4\n\t\tc'8\n\t\td'8\n\t\t\\revert Staff.TimeSignature #'stencil\n\t}\n\t{\n\t\t\\override Staff.TimeSignature #'stencil = ##f\n\t\t\\time 3/8\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\t\\revert Staff.TimeSignature #'stencil\n\t}\n\t{\n\t\t\\override Staff.TimeSignature #'stencil = ##f\n\t\t\\time 1/4\n\t\tc'8\n\t\td'8\n\t\t\\revert Staff.TimeSignature #'stencil\n\t}\n}"
