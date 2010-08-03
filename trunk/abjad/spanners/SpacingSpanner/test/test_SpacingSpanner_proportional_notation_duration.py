from abjad import *


def test_SpacingSpanner_proportional_notation_duration_01( ):
   '''You can set LilyPond Score.proportionalNotationDuration
   directly on the Abjad spacing spanner. Make sure to start
   a new spacing section, too.'''

   t = Staff(macros.scale(4))
   spacing_spanner_1 = SpacingSpanner(t[:2])
   spacing_spanner_1.new_section = True
   spacing_spanner_1.proportional_notation_duration = Rational(1, 15)
   spacing_spanner_2 = SpacingSpanner(t[2:])
   spacing_spanner_2.new_section = True
   spacing_spanner_2.proportional_notation_duration = Rational(1, 30)
   
   r'''
   \new Staff {
           \newSpacingSection
           \set Score.proportionalNotationDuration = #(ly:make-moment 1 15)
           c'8
           d'8
           %%% spacing section ends here %%%
           \newSpacingSection
           \set Score.proportionalNotationDuration = #(ly:make-moment 1 30)
           e'8
           f'8
           %%% spacing section ends here %%%
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\newSpacingSection\n\t\\set Score.proportionalNotationDuration = #(ly:make-moment 1 15)\n\tc'8\n\td'8\n\t%%% spacing section ends here %%%\n\t\\newSpacingSection\n\t\\set Score.proportionalNotationDuration = #(ly:make-moment 1 30)\n\te'8\n\tf'8\n\t%%% spacing section ends here %%%\n}"
