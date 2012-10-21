from abjad import *


def test_LayoutBlock_lilypond_command_mark_01():

    staff = Staff("fs'2 fs'2 gs'2 gs'2")
    score = Score([staff])
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    lilypond_file.layout_block.append(marktools.LilyPondCommandMark('accidentalStyle forget'))

    assert lilypond_file.layout_block.lilypond_format == '\\layout {\n\t\\accidentalStyle forget\n}'
