from abjad import *


def test_LeafSelection_replace_with_01():
    '''Works on Abjad components.
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
