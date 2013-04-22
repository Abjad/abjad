from abjad import *


def test_LayoutBlock_01():

    lb = lilypondfiletools.LayoutBlock()
    lb.indent = 0
    lb.ragged_right = True

    r'''
    \layout {
        indent = #0
        ragged-right = ##t
    }
    '''

    assert lb.lilypond_format == '\\layout {\n\tindent = #0\n\tragged-right = ##t\n}'


def test_LayoutBlock_02():

    lb = lilypondfiletools.LayoutBlock()
    m = marktools.LilyPondCommandMark('accidentalStyle modern')
    lb.append(m)

    r'''
    \layout {
        \accidentalStyle modern
    }
    '''

    assert lb.lilypond_format == '\\layout {\n\t\\accidentalStyle modern\n}'
