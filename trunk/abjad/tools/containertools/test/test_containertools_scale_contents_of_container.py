# -*- encoding: utf-8 -*-
from abjad import *


def test_containertools_scale_contents_of_container_01():
    r'''Scale leaves in voice by 3/2; ie, dot leaves.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(voice, Duration(3, 2))

    r'''
    \new Voice {
        c'8.
        d'8.
        e'8.
        f'8.
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8.
            d'8.
            e'8.
            f'8.
        }
        '''
        )


def test_containertools_scale_contents_of_container_02():
    r'''Scale leaves in voice by 5/4; ie, quarter-tie leaves.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(voice, Duration(5, 4))

    r'''
    \new Voice {
        c'8 ~
        c'32
        d'8 ~
        d'32
        e'8 ~
        e'32
        f'8 ~
        f'32
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 ~
            c'32
            d'8 ~
            d'32
            e'8 ~
            e'32
            f'8 ~
            f'32
        }
        '''
        )


def test_containertools_scale_contents_of_container_03():
    r'''Scale leaves in voice by untied 4/3; ie, tupletize notes.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(voice, Duration(4, 3))

    r'''
    \new Voice {
        \times 2/3 {
            c'4
        }
        \times 2/3 {
            d'4
        }
        \times 2/3 {
            e'4
        }
        \times 2/3 {
            f'4
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            \times 2/3 {
                c'4
            }
            \times 2/3 {
                d'4
            }
            \times 2/3 {
                e'4
            }
            \times 2/3 {
                f'4
            }
        }
        '''
        )


def test_containertools_scale_contents_of_container_04():
    r'''Scale leaves in voice by tied 5/4 (tied and without power-of-two denominator);
    ie, tupletize notes.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(voice, Duration(5, 6))

    r'''
    \new Voice {
        \times 2/3 {
            c'8 ~
            c'32
        }
        \times 2/3 {
            d'8 ~
            d'32
        }
        \times 2/3 {
            e'8 ~
            e'32
        }
        \times 2/3 {
            f'8 ~
            f'32
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 ~
                c'32
            }
            \times 2/3 {
                d'8 ~
                d'32
            }
            \times 2/3 {
                e'8 ~
                e'32
            }
            \times 2/3 {
                f'8 ~
                f'32
            }
        }
        '''
        )


def test_containertools_scale_contents_of_container_05():
    r'''Scale mixed notes and tuplets.
    '''

    voice = Voice([Note(0, (3, 16)),
        tuplettools.FixedDurationTuplet(Duration(3, 8), notetools.make_repeated_notes(4))])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)

    r'''
    \new Voice {
        c'8.
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 3/4 {
            d'8
            e'8
            f'8
            g'8
        }
    }
    '''

    containertools.scale_contents_of_container(voice, Duration(2, 3))

    r'''
    \new Voice {
        c'8
        {
            d'16
            e'16
            f'16
            g'16
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8
            {
                d'16
                e'16
                f'16
                g'16
            }
        }
        '''
        )


def test_containertools_scale_contents_of_container_06():
    r'''Undo scale of 5/4 with scale of 4/5.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    containertools.scale_contents_of_container(voice, Duration(5, 4))

    r'''
    \new Voice {
        c'8 ~
        c'32
        d'8 ~
        d'32
        e'8 ~
        e'32
        f'8 ~
        f'32
    }
    '''

    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 ~
            c'32
            d'8 ~
            d'32
            e'8 ~
            e'32
            f'8 ~
            f'32
        }
        '''
        )

    containertools.scale_contents_of_container(voice, Duration(4, 5))

    r'''
    \new Voice {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )


def test_containertools_scale_contents_of_container_07():
    r'''Double all contents, including measure.
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

    containertools.scale_contents_of_container(voice, Duration(2))
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    r'''
    \new Voice {
        {
            \time 2/4
            c'4
            d'4
        }
        {
            \time 2/4
            e'4
            f'4
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            {
                \time 2/4
                c'4
                d'4
            }
            {
                \time 2/4
                e'4
                f'4
            }
        }
        '''
        )


def test_containertools_scale_contents_of_container_08():
    r'''Multiply all contents by 5/4, including measure.
    '''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

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

    containertools.scale_contents_of_container(t, Duration(5, 4))
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Voice {
        {
            \time 20/64
            c'8 ~
            c'32
            d'8 ~
            d'32
        }
        {
            \time 20/64
            e'8 ~
            e'32
            f'8 ~
            f'32
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            {
                \time 20/64
                c'8 ~
                c'32
                d'8 ~
                d'32
            }
            {
                \time 20/64
                e'8 ~
                e'32
                f'8 ~
                f'32
            }
        }
        '''
        )
