from abjad import *


def test_spacing_interface_proportional_notation_duration_01( ):
   '''You can set the LilyPond propotionalNotationDuration context
   setting scorewide on any Abjad score.'''

   t = Score([Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))])
   t.spacing.proportional_notation_duration = Rational(1, 56)

   r'''
   \new Score \with {
           proportionalNotationDuration = #(ly:make-moment 1 56)
   } <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>
   '''

   assert check.wf(t)
   assert t.format == "\\new Score \\with {\n\tproportionalNotationDuration = #(ly:make-moment 1 56)\n} <<\n\t\\new Staff {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n>>"
