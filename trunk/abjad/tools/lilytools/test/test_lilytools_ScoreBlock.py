from abjad import *


def test_lilytools_ScoreBlock_01( ):

   score = Score([Staff(construct.scale(4))])
   score_block = lilytools.ScoreBlock( )
   layout_block = lilytools.LayoutBlock( )
   midi_block = lilytools.MidiBlock( )

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
