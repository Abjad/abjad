from abjad import *


def test_Spanner___len___01():
    '''Spanner length equals length of components.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner(t[1])

    r'''
    \new Voice {
        {
            c'8
            d'8
        }
        {
            e'8 [
            f'8 ]
        }
        {
            g'8
            a'8
        }
    }
    '''

    assert len(p) == 1
    assert len(p.components) == 1
    assert len(p.leaves) == 2


def test_Spanner___len___02():
    '''Spanner length equals length of components.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8 ]
        }
    }
    '''

    assert len(p) == 3
    assert len(p.components) == 3
    assert len(p.leaves) == 6
