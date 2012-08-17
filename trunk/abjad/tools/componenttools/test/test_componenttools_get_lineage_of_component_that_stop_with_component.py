from abjad import *


def test_componenttools_get_lineage_of_component_that_stop_with_component_01( ):

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8
        }
    }
    '''

    result = componenttools.get_lineage_of_component_that_stop_with_component(t)

    "[Voice{3}, Container(g'8, a'8), Note(a', 8)]"

    assert len(result) == 3
    assert t in result
    assert t[-1] in result
    assert t[-1][-1] in result

    result = componenttools.get_lineage_of_component_that_stop_with_component(t[-1])

    "[Container(g'8, a'8), Note(a', 8), Voice{3}]"

    assert len(result) == 3
    assert t in result
    assert t[-1] in result
    assert t[-1][-1] in result

    result = componenttools.get_lineage_of_component_that_stop_with_component(t[-1][-1])

    "[Note(a', 8), Container(g'8, a'8), Voice{3}]"

    assert len(result) == 3
    assert t in result
    assert t[-1] in result
    assert t[-1][-1] in result
