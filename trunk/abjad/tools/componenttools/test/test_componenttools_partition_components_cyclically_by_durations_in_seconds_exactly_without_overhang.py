from abjad import *


def test_componenttools_partition_components_cyclically_by_durations_in_seconds_exactly_without_overhang_01( ):
    '''Read durations cyclically.
    If components remain, do not append final part.'''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    contexttools.TempoMark(Duration(1, 4), 60, target_context = Staff)(t)

    r'''
    \new Staff {
            \time 2/8
            \tempo 4=60
            c'8
            d'8
            \time 2/8
            e'8
            f'8
            \time 2/8
            g'8
            a'8
            \time 2/8
            b'8
            c''8
            %% tempo 4=60 ends here
    }
    '''

    groups = componenttools.partition_components_cyclically_by_durations_in_seconds_exactly_without_overhang(t.leaves, [1.5])

    "[[Note(c'', 8), Note(b', 8), Note(a', 8)], [Note(g', 8), Note(f', 8), Note(e', 8)]]"

    assert len(groups) == 2
    assert groups[0] == list(t.leaves[:3])
    assert groups[1] == list(t.leaves[3:6])
