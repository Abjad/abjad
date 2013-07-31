from abjad import *


def test_SequentialLeafSelection_replace_with_01():
    r'''Replace with rests.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    selection = t.select_leaves()
    selection.replace_with(Rest)

    r'''
    \new Staff {
        r8
        r8
        r8
        r8
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == '\\new Staff {\n\tr8\n\tr8\n\tr8\n\tr8\n}'


def test_SequentialLeafSelection_replace_with_02():
    r'''Replace with skips.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    selection = t.select_leaves()
    selection.replace_with(skiptools.Skip)

    r'''
    \new Staff {
        s8
        s8
        s8
        s8
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == '\\new Staff {\n\ts8\n\ts8\n\ts8\n\ts8\n}'
