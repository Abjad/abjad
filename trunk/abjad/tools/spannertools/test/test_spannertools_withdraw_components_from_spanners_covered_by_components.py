from abjad import *


def test_spannertools_withdraw_components_from_spanners_covered_by_components_01():
    '''Withdraw from all spanners covered by components.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:2])
    spannertools.SlurSpanner(t[:])

    r'''
    \new Voice {
        c'8 [ (
        d'8 ]
        e'8
        f'8 )
    }
    '''

    spannertools.withdraw_components_from_spanners_covered_by_components(t[:2])

    r'''
    \new Voice {
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"
