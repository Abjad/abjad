from abjad import *


def test_SpacingSpanner_proportional_notation_duration_01( ):
   '''You can set LilyPond Score.proportionalNotationDuration
   directly on the Abjad spacing spanner. Make sure to start
   a new spacing section, too.
   '''

#   t = Staff(macros.scale(4))
#   spacing_spanner_1 = spannertools.SpacingSpanner(t[:2])
#   spacing_spanner_1.new_section = True
#   spacing_spanner_1.proportional_notation_duration = Fraction(1, 15)
#   spacing_spanner_2 = spannertools.SpacingSpanner(t[2:])
#   spacing_spanner_2.new_section = True
#   spacing_spanner_2.proportional_notation_duration = Fraction(1, 30)

   t = Staff(macros.scale(4))
   marktools.LilyPondCommandMark('new_spacing_section')(t[0])
   t[0].set.score.proportional_notation_duration = schemetools.SchemeMoment(Fraction(1, 15))
   marktools.LilyPondCommandMark('new_spacing_section')(t[2])
   t[2].set.score.proportional_notation_duration = schemetools.SchemeMoment(Fraction(1, 30))
   
   r'''
   \new Staff {
           \set Score.proportionalNotationDuration = #(ly:make-moment 1 15)
           \newSpacingSection
           c'8
           d'8
           \set Score.proportionalNotationDuration = #(ly:make-moment 1 30)
           \newSpacingSection
           e'8
           f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\set Score.proportionalNotationDuration = #(ly:make-moment 1 15)\n\t\\newSpacingSection\n\tc'8\n\td'8\n\t\\set Score.proportionalNotationDuration = #(ly:make-moment 1 30)\n\t\\newSpacingSection\n\te'8\n\tf'8\n}"
