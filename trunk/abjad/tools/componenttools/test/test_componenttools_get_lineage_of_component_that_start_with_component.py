from abjad import *


def test_componenttools_get_lineage_of_component_that_start_with_component_01( ):

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

    result = componenttools.get_lineage_of_component_that_start_with_component(t)

    "[Voice{3}, Container(c'8, d'8), Note(c', 8)]"

    assert len(result) == 3
    assert t in result
    assert t[0] in result
    assert t[0][0] in result

    result = componenttools.get_lineage_of_component_that_start_with_component(t[0])

    "[Container(c'8, d'8), Note(c', 8), Voice{3}]"

    assert len(result) == 3
    assert t in result
    assert t[0] in result
    assert t[0][0] in result

    result = componenttools.get_lineage_of_component_that_start_with_component(t[0][0])

    "[Note(c', 8), Container(c'8, d'8), Voice{3}]"

    assert len(result) == 3
    assert t in result
    assert t[0] in result
    assert t[0][0] in result
