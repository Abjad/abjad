from abjad import *


def test_componenttools_partition_components_by_durations_ge_01():

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
        {
            \time 2/8
            b'8
            c''8
        }
    }
    '''

    parts = componenttools.partition_components_by_durations_ge(
        staff.leaves, [Duration(3, 16), Duration(1, 16)], cyclic=True, in_seconds=False, overhang=True)

    "[[Note(c', 8), Note(d', 8)], "
    "[Note(e', 8)], [Note(f', 8), Note(g', 8)], "
    "[Note(a', 8)], [Note(b', 8), Note(c'', 8)]]"

    assert len(parts) == 5
    assert parts[0] == list(staff.leaves[:2])
    assert parts[1] == list(staff.leaves[2:3])
    assert parts[2] == list(staff.leaves[3:5])
    assert parts[3] == list(staff.leaves[5:6])
    assert parts[4] == list(staff.leaves[6:])
