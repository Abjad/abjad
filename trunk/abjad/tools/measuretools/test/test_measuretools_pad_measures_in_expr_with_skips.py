# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_measuretools_pad_measures_in_expr_with_skips_01():

    staff = Staff(2 * Measure((2, 8), "c'8 d'8"))

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            c'8
            d'8
        }
    }
    '''

    measuretools.pad_measures_in_expr_with_skips(staff, Duration(1, 32), Duration(1, 64))

    r'''
    \new Staff {
        {
            \time 19/64
            s32
            c'8
            d'8
            s64
        }
        {
            s32
            c'8
            d'8
            s64
        }
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 19/64
                s32
                c'8
                d'8
                s64
            }
            {
                s32
                c'8
                d'8
                s64
            }
        }
        '''
        )


def test_measuretools_pad_measures_in_expr_with_skips_02():
    r'''Works when measures contain stacked voices.
    '''

    measure = Measure((2, 8), 2 * Voice(notetools.make_repeated_notes(2)))
    measure.is_simultaneous = True
    staff = Staff(measure * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        <<
            \time 1/4
            \new Voice {
                c'8
                d'8
            }
            \new Voice {
                e'8
                f'8
            }
        >>
        <<
            \time 1/4
            \new Voice {
                g'8
                a'8
            }
            \new Voice {
                b'8
                c''8
            }
        >>
    }
    '''

    measuretools.pad_measures_in_expr_with_skips(staff, Duration(1, 32), Duration(1, 64))

    r'''
    \new Staff {
        <<
            \time 19/64
            \new Voice {
                s32
                c'8
                d'8
                s64
            }
            \new Voice {
                s32
                e'8
                f'8
                s64
            }
        >>
        <<
            \time 19/64
            \new Voice {
                s32
                g'8
                a'8
                s64
            }
            \new Voice {
                s32
                b'8
                c''8
                s64
            }
        >>
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            <<
                \time 19/64
                \new Voice {
                    s32
                    c'8
                    d'8
                    s64
                }
                \new Voice {
                    s32
                    e'8
                    f'8
                    s64
                }
            >>
            <<
                \time 19/64
                \new Voice {
                    s32
                    g'8
                    a'8
                    s64
                }
                \new Voice {
                    s32
                    b'8
                    c''8
                    s64
                }
            >>
        }
        '''
        )


def test_measuretools_pad_measures_in_expr_with_skips_03():
    r'''Set splice to true to extend edge spanners over newly insert rests.
    '''

    measure = Measure((2, 8), "c'8 d'8")
    spannertools.BeamSpanner(measure[:])
    measuretools.pad_measures_in_expr_with_skips(
        measure, Duration(1, 32), Duration(1, 64), splice=True)

    r'''
    {
        \time 19/64
        s32 [
        c'8
        d'8
        s64 ]
    }
    '''

    assert inspect(measure).is_well_formed()
    assert testtools.compare(
        measure,
        r'''
        {
            \time 19/64
            s32 [
            c'8
            d'8
            s64 ]
        }
        '''
        )
