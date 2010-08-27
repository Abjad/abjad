from abjad import *


def test_BarNumberInterface_current_bar_number_01( ):
   '''Handle LilyPond currentBarNumber context setting on note.'''

   t = Staff(macros.scale(4))
   t[0].set.score.current_bar_number = 12

   r'''
   \new Staff {
           \set Score.currentBarNumber = #12
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\set Score.currentBarNumber = #12\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_BarNumberInterface_current_bar_number_02( ):
   '''Handle LilyPond currentBarNumber context setting on measure.'''

   t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
   macros.diatonicize(t)
   t[0].set.score.current_bar_number = 12

   r'''
   \new Staff {
           {
                   \set Score.currentBarNumber = #12
                   \time 2/8
                   c'8
                   d'8
           }
           {
                   \time 2/8
                   e'8
                   f'8
           }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\set Score.currentBarNumber = #12\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t}\n}"
