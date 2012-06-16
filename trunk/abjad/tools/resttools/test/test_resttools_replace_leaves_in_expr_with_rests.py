from abjad import *


def test_resttools_replace_leaves_in_expr_with_rests_01():
    '''Works on Abjad components.'''

    t = Staff("c'8 d'8 e'8 f'8")
    resttools.replace_leaves_in_expr_with_rests(t)

    r'''
    \new Staff {
        r8
        r8
        r8
        r8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == '\\new Staff {\n\tr8\n\tr8\n\tr8\n\tr8\n}'


def test_resttools_replace_leaves_in_expr_with_rests_02():
    '''Works on Python lists of Abjad components.'''

    t = Staff("c'8 d'8 e'8 f'8")
    resttools.replace_leaves_in_expr_with_rests(t[:])

    r'''
    \new Staff {
        r8
        r8
        r8
        r8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == '\\new Staff {\n\tr8\n\tr8\n\tr8\n\tr8\n}'
