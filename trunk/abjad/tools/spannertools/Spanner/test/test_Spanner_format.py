from abjad import *


def test_Spanner_format_01():
    '''Base Spanner class makes no format-time contributions.
    However, base spanner causes no explosions at format-time, either.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    p = spannertools.Spanner(t[:])

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
