# -*- encoding: utf-8 -*-
from abjad import *


def test_Spanner___len___01():
    r'''Spanner length equals length of components.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[1])

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

    assert len(beam) == 1
    assert len(beam.components) == 1
    assert len(beam.leaves) == 2


def test_Spanner___len___02():
    r'''Spanner length equals length of components.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:])

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

    assert len(beam) == 3
    assert len(beam.components) == 3
    assert len(beam.leaves) == 6
