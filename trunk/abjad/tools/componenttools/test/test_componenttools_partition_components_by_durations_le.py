from abjad import *


def test_componenttools_partition_components_by_durations_le_01():

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    contexttools.TempoMark(Duration(1, 4), 60, target_context=Staff)(t)

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

    parts = componenttools.partition_components_by_durations_le(
        t.leaves, [0.75], cyclic=True, in_seconds=True, overhang=False)

    "[[Note(c', 8)], [Note(d', 8)], [Note(e', 8)], [Note(f', 8)], [Note(g', 8)], [Note(a', 8)], [Note(b', 8)]]"

    assert len(parts) == 7
    assert parts[0] == list(t.leaves[:1])
    assert parts[1] == list(t.leaves[1:2])
    assert parts[2] == list(t.leaves[2:3])
    assert parts[3] == list(t.leaves[3:4])
    assert parts[4] == list(t.leaves[4:5])
    assert parts[5] == list(t.leaves[5:6])
    assert parts[6] == list(t.leaves[6:7])


def test_componenttools_partition_components_by_durations_le_02():

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
            \time 2/8
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
    }
    '''

    parts = componenttools.partition_components_by_durations_le(
        t.leaves, [Duration(3, 16)], cyclic=True, in_seconds=False, overhang=False)

    "[[Note(c', 8)], [Note(d', 8)], [Note(e', 8)], [Note(f', 8)], "
    "[Note(g', 8)], [Note(a', 8)], [Note(b', 8)]]"

    assert len(parts) == 7
    assert parts[0] == list(t.leaves[:1])
    assert parts[1] == list(t.leaves[1:2])
    assert parts[2] == list(t.leaves[2:3])
    assert parts[3] == list(t.leaves[3:4])
    assert parts[4] == list(t.leaves[4:5])
    assert parts[5] == list(t.leaves[5:6])
    assert parts[6] == list(t.leaves[6:7])


def test_componenttools_partition_components_by_durations_le_03():

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
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

    parts = componenttools.partition_components_by_durations_le(
            t.leaves, [0.75], cyclic=False, in_seconds=True, overhang=False)

    "[[Note(c', 8)]]"

    assert len(parts) == 1
    assert parts[0] == list(t.leaves[:1])


def test_componenttools_partition_components_by_durations_le_04():

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
            \time 2/8
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
    }
    '''

    parts = componenttools.partition_components_by_durations_le(
        t.leaves, [Duration(3, 16)], cyclic=False, in_seconds=False, overhang=False)

    "[[Note(c', 8)]]"

    assert len(parts) == 1
    assert parts[0] == list(t.leaves[:1])
