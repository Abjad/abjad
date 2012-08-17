from abjad import *


def test_componenttools_get_improper_descendents_of_component_that_cross_offset_01():
    '''Staff and first measure cross offset at 1/8.'''

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

    result = componenttools.get_improper_descendents_of_component_that_cross_offset(t, Duration(1, 8))

    assert result == [t, t[0]]


def test_componenttools_get_improper_descendents_of_component_that_cross_offset_02():
    '''Staff, first measure and first note cross 1/16.'''

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

    result = componenttools.get_improper_descendents_of_component_that_cross_offset(t, Duration(1, 16))

    assert result == [t, t[0], t[0][0]]


def test_componenttools_get_improper_descendents_of_component_that_cross_offset_03():
    '''Nothing crosses 0.'''

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

    result = componenttools.get_improper_descendents_of_component_that_cross_offset(t, Duration(0))

    assert result == []


def test_componenttools_get_improper_descendents_of_component_that_cross_offset_04():
    '''Nothing crosses 100.'''

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

    result = componenttools.get_improper_descendents_of_component_that_cross_offset(t, Duration(100))

    assert result == []
