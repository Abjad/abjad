# -*- encoding: utf-8 -*-
from abjad import *


def test_containertools_repeat_last_n_elements_of_container_01():
    r'''Cyclic extend measures in voice.
    '''

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)

    r'''
    \new Voice {
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
    }
    '''

    containertools.repeat_last_n_elements_of_container(voice, n=1, total=4)
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    r'''
    \new Voice {
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
            e'8
            f'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
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
                e'8
                f'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
        }
        '''
        )


def test_containertools_repeat_last_n_elements_of_container_02():
    r'''Cyclic extend tuplets in voice.
    '''

    voice = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)

    r'''
    \new Voice {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    containertools.repeat_last_n_elements_of_container(voice, 2, total=2)

    r'''
    \new Voice {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8
            }
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8
            }
        }
        '''
        )
