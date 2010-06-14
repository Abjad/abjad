from abjad import *


def test_rigid_measure_parallel_01( ):
   '''Rigid measures may be hold parallel contents.'''

   measure = RigidMeasure((2, 8), Voice(leaftools.make_repeated_notes(2)) * 2)
   measure.parallel = True
   measure[0].voice.number = 1
   measure[1].voice.number = 2
   t = Staff([measure])
   pitchtools.diatonicize(t)

   r'''
   \new Staff {
           <<
                   \time 2/8
                   \new Voice {
                           \voiceOne
                           c'8
                           d'8
                   }
                   \new Voice {
                           \voiceTwo
                           e'8
                           f'8
                   }
           >>
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t<<\n\t\t\\time 2/8\n\t\t\\new Voice {\n\t\t\t\\voiceOne\n\t\t\tc'8\n\t\t\td'8\n\t\t}\n\t\t\\new Voice {\n\t\t\t\\voiceTwo\n\t\t\te'8\n\t\t\tf'8\n\t\t}\n\t>>\n}"
