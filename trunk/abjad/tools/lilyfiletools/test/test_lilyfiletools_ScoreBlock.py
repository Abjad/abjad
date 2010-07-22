from abjad import *


def test_lilyfiletools_ScoreBlock_01( ):

   score = Score([Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))])
   score_block = lilyfiletools.ScoreBlock( )
   layout_block = lilyfiletools.LayoutBlock( )
   midi_block = lilyfiletools.MidiBlock( )

   score_block.append(score)
   score_block.append(layout_block)
   score_block.append(midi_block)
   
   r'''
   \score {
           \new Score <<
                   \new Staff {
                           c'8
                           d'8
                           e'8
                           f'8
                   }
           >>
           \layout { }
           \midi { }
   }
   '''

   assert score_block.format == "\\score {\n\t\\new Score <<\n\t\t\\new Staff {\n\t\t\tc'8\n\t\t\td'8\n\t\t\te'8\n\t\t\tf'8\n\t\t}\n\t>>\n\t\\layout { }\n\t\\midi { }\n}"
