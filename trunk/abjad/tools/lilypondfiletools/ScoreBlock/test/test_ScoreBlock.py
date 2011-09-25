from abjad import *


def test_ScoreBlock_01():
    '''Midi block is formatted when empty by default.
    Layout block must be explicitly set to format when empty.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    score_block = lilypondfiletools.ScoreBlock()
    layout_block = lilypondfiletools.LayoutBlock()
    layout_block.is_formatted_when_empty = True
    midi_block = lilypondfiletools.MIDIBlock()

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
        \layout {}
        \midi {}
    }
    '''

    assert score_block.format == "\\score {\n\t\\new Score <<\n\t\t\\new Staff {\n\t\t\tc'8\n\t\t\td'8\n\t\t\te'8\n\t\t\tf'8\n\t\t}\n\t>>\n\t\\layout {}\n\t\\midi {}\n}"
