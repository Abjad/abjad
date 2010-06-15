from abjad import *


def test_scoretools_set_accidental_style_01( ):

   score = Score(Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(2)) * 2)
   scoretools.set_accidental_style(score, 'forget')

   r'''
   \new Score <<
        \new Staff {
                #(set-accidental-style 'forget)
                c'8
                d'8
        }
        \new Staff {
                #(set-accidental-style 'forget)
                c'8
                d'8
        }
   >>
   '''

   assert componenttools.is_well_formed_component(score)
   assert score.format == "\\new Score <<\n\t\\new Staff {\n\t\t#(set-accidental-style 'forget)\n\t\tc'8\n\t\td'8\n\t}\n\t\\new Staff {\n\t\t#(set-accidental-style 'forget)\n\t\tc'8\n\t\td'8\n\t}\n>>"
