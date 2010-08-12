from abjad import *


def test_BarNumberInterface_current_01( ):
   '''Handle LilyPond ``currentBarNumber`` context setting on note.'''

   t = Staff(macros.scale(4))
   t[0].bar_number.current = 12
   overridetools.promote_attribute_to_context_on_grob_handler(t[0].bar_number, 'current', 'Score')

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


def test_BarNumberInterface_current_02( ):
   '''Handle LilyPond ``currentBarNumber`` context setting on measure.'''

   t = Staff(RigidMeasure((2, 8), notetools.make_repeated_notes(2)) * 2)
   macros.diatonicize(t)
   t[0].bar_number.current = 12
   overridetools.promote_attribute_to_context_on_grob_handler(t[0].bar_number, 'current', 'Score')

   r'''
   \new Staff {
           {
                   \time 2/8
                   \set Score.currentBarNumber = #12
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
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\t\\set Score.currentBarNumber = #12\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t}\n}"
