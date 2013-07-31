from abjad import *


def test_Component_select_descendants_01():
    r'''Staff and first measure cross offset at 1/8.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
            \time 2/8
            c'8
            d'8
            \time 2/8
            e'8
            f'8
    }
    '''

    cross_offset = t.timespan.start_offset + Duration(1, 8)
    result = t.select_descendants(cross_offset=cross_offset)

    assert result == [t, t[0]]


def test_Component_select_descendants_02():
    r'''Staff, first measure and first note cross 1/16.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
            \time 2/8
            c'8
            d'8
            \time 2/8
            e'8
            f'8
    }
    '''

    cross_offset = t.timespan.start_offset + Duration(1, 16)
    result = t.select_descendants(cross_offset=cross_offset)

    assert result == [t, t[0], t[0][0]]


def test_Component_select_descendants_03():
    r'''Nothing crosses 0.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
            \time 2/8
            c'8
            d'8
            \time 2/8
            e'8
            f'8
    }
    '''

    cross_offset = t.timespan.start_offset + Duration(0)
    result = t.select_descendants(cross_offset=cross_offset)

    assert result == []


def test_Component_select_descendants_04():
    r'''Nothing crosses 100.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Staff {
            \time 2/8
            c'8
            d'8
            \time 2/8
            e'8
            f'8
    }
    '''

    cross_offset = t.timespan.start_offset + Duration(100)
    result = t.select_descendants(cross_offset=cross_offset)

    assert result == []
