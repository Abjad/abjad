from abjad import *
import py.test


def test_Measure_parallel_01( ):
   '''Rigid measures may be hold parallel contents.'''

   py.test.skip('fix minor format positioning of time signatures.')
   measure = Measure((2, 8), Voice(notetools.make_repeated_notes(2)) * 2)
   measure.is_parallel = True
   #measure[0].voice.number = 1
   #measure[1].voice.number = 2
   marktools.LilyPondCommandMark('voiceOne')(measure[0])
   marktools.LilyPondCommandMark('voiceTwo')(measure[1])
     
   t = Staff([measure])
   macros.diatonicize(t)

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

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t<<\n\t\t\\time 2/8\n\t\t\\new Voice {\n\t\t\t\\voiceOne\n\t\t\tc'8\n\t\t\td'8\n\t\t}\n\t\t\\new Voice {\n\t\t\t\\voiceTwo\n\t\t\te'8\n\t\t\tf'8\n\t\t}\n\t>>\n}"
