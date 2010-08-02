from abjad import *


def test_tempo_proportional_spanner_01( ):
   '''Do special things with tempo and spacing.'''

   t = Score([Staff(macros.scale(4))])
   tempo_indication = tempotools.TempoIndication(Rational(1, 4), 60)
   spacing_indication = spacingtools.SpacingIndication(tempo_indication, Rational(1, 34))
   t.spacing.scorewide = spacing_indication

   p = TempoSpannerProportional(t[0][:2])
   p.tempo_indication = tempotools.TempoIndication(Rational(1, 4), 60)
   p = TempoSpannerProportional(t[0][2:])
   p.tempo_indication = tempotools.TempoIndication(Rational(1, 4), 120)

   r'''
   \new Score <<
        \new Staff {
             \tempo 4=60
             \newSpacingSection
             \set Score.proportionalNotationDuration = #(ly:make-moment 1 . 34)
             c'8
             d'8
             %% tempo 4=60 ends here
             \tempo 4=120
             \newSpacingSection
             \set Score.proportionalNotationDuration = #(ly:make-moment 1 . 17)
             \tempo 4=120
             e'8
             f'8
             %% tempo 4=120 ends here
        }
   >>
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Score <<\n\t\\new Staff {\n\t\t\\tempo 4=60\n\t\t\\newSpacingSection\n\t\t\\set Score.proportionalNotationDuration = #(ly:make-moment 1 34)\n\t\tc'8\n\t\td'8\n\t\t%% tempo 4=60 ends here\n\t\t\\tempo 4=120\n\t\t\\newSpacingSection\n\t\t\\set Score.proportionalNotationDuration = #(ly:make-moment 1 17)\n\t\te'8\n\t\tf'8\n\t\t%% tempo 4=120 ends here\n\t}\n>>"
