# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_measuretools_fuse_measures_01():
    r'''Fuse unicorporated measures carrying
    time signatures with power-of-two denominators.
    '''
    
    t1 = Measure((1, 8), "c'16 d'16")
    spannertools.BeamSpanner(t1[:])
    t2 = Measure((2, 16), "c'16 d'16")
    spannertools.SlurSpanner(t2[:])
    staff = Staff([t1, t2])

    r'''
    \new Staff {
        {
            \time 1/8
            c'16 [
            d'16 ]
        }
        {
            \time 2/16
            c'16 (
            d'16 )
        }
    }
    '''

    new = measuretools.fuse_measures(staff[:])

    r'''
    \new Staff {
        {
            \time 2/8
            c'16 [
            d'16 ]
            c'16 (
            d'16 )
        }
    }
    '''

    assert new is not t1 and new is not t2
    assert len(t1) == 0
    assert len(t2) == 0
    assert select(new).is_well_formed()
    assert testtools.compare(
        new.lilypond_format,
        r'''
        {
            \time 2/8
            c'16 [
            d'16 ]
            c'16 (
            d'16 )
        }
        '''
        )


def test_measuretools_fuse_measures_02():
    r'''Fuse measures carrying time signatures with differing power-of-two denominators.
    Helpers selects minimum of two denominators.
    Beams are OK because they attach to leaves rather than containers.
    '''

    t = Voice(measuretools.make_measures_with_full_measure_spacer_skips([(1, 8), (2, 16)]))
    measuretools.fill_measures_in_expr_with_repeated_notes(t, Duration(1, 16))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t.select_leaves())

    r'''
    \new Voice {
        {
            \time 1/8
            c'16 [
            d'16
        }
        {
            \time 2/16
            e'16
            f'16 ]
        }
    }
    '''

    measuretools.fuse_measures(t[:])

    r'''
    \new Voice {
        {
            \time 2/8
            c'16 [
            d'16
            e'16
            f'16 ]
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            {
                \time 2/8
                c'16 [
                d'16
                e'16
                f'16 ]
            }
        }
        '''
        )


def test_measuretools_fuse_measures_03():
    r'''Fuse measures with differing power-of-two denominators.
    Helpers selects minimum of two denominators.
    Beam attaches to container rather than leaves.
    '''

    t = Voice(measuretools.make_measures_with_full_measure_spacer_skips([(1, 8), (2, 16)]))
    measuretools.fill_measures_in_expr_with_repeated_notes(t, Duration(1, 16))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t[0])

    r'''
    \new Voice {
        {
            \time 1/8
            c'16 [
            d'16 ]
        }
        {
            \time 2/16
            e'16
            f'16
        }
    }
    '''

    measuretools.fuse_measures(t[:])

    r'''
    \new Voice {
        {
            \time 2/8
            c'16
            d'16
            e'16
            f'16
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            {
                \time 2/8
                c'16
                d'16
                e'16
                f'16
            }
        }
        '''
        )


def test_measuretools_fuse_measures_04():
    r'''Fuse measures with power-of-two-denominators together with measures
    without power-of-two denominators.
    Helpers selects least common multiple of denominators.
    Beams are OK because they attach to leaves rather than containers.
    '''

    m1 = Measure((1, 8), notetools.make_repeated_notes(1))
    m2 = Measure((1, 12), notetools.make_repeated_notes(1))
    t = Voice([m1, m2])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t.select_leaves())

    r'''
    \new Voice {
        {
            \time 1/8
            c'8 [
        }
        {
            \time 1/12
            \scaleDurations #'(2 . 3) {
                d'8 ]
            }
        }
    }
    '''

    measuretools.fuse_measures(t[:])

    r'''
    \new Voice {
        {
            \time 5/24
            \scaleDurations #'(2 . 3) {
                c'8. [
                d'8 ]
            }
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            {
                \time 5/24
                \scaleDurations #'(2 . 3) {
                    c'8. [
                    d'8 ]
                }
            }
        }
        '''
        )


def test_measuretools_fuse_measures_05():
    r'''Fusing empty selection returns none.
    '''

    staff = Staff()
    result = measuretools.fuse_measures(staff[:])
    assert result is None


def test_measuretools_fuse_measures_06():
    r'''Fusing selection of only one measure returns measure unaltered.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    staff = Staff([measure])
    new = measuretools.fuse_measures(staff[:])

    assert new is measure


def test_measuretools_fuse_measures_07():
    r'''Fuse three measures.
    '''

    t = Voice(measuretools.make_measures_with_full_measure_spacer_skips([(1, 8), (1, 8), (1, 8)]))
    measuretools.fill_measures_in_expr_with_repeated_notes(t, Duration(1, 16))
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t.select_leaves())

    r'''
    \new Voice {
        {
            \time 1/8
            c'16 [
            d'16
        }
        {
            \time 1/8
            e'16
            f'16
        }
        {
            \time 1/8
            g'16
            a'16 ]
        }
    }
    '''

    measuretools.fuse_measures(t[:])

    r'''
    \new Voice {
        {
            \time 3/8
            c'16 [
            d'16
            e'16
            f'16
            g'16
            a'16 ]
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            {
                \time 3/8
                c'16 [
                d'16
                e'16
                f'16
                g'16
                a'16 ]
            }
        }
        '''
        )


def test_measuretools_fuse_measures_08():
    r'''Measure fusion across intervening container boundaries is undefined.
    '''

    t = Voice(Container(Measure((2, 8), notetools.make_repeated_notes(2)) * 2) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Voice {
        {
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
        {
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
    }
    '''

    assert py.test.raises(AssertionError, 'measuretools.fuse_measures([t[0][1], t[1][0]])')


def test_measuretools_fuse_measures_09():
    r'''Fusing measures with power-of-two denominators
    to measures without power-of-two denominators.
    With change in number of note heads because of non-power-of-two multiplier.
    '''

    t = Staff([
        Measure((9, 80), []),
        Measure((2, 16), [])])
    measuretools.fill_measures_in_expr_with_time_signature_denominator_notes(t)

    r'''
    \new Staff {
        {
            \time 9/80
            \scaleDurations #'(4 . 5) {
                c'64
                c'64
                c'64
                c'64
                c'64
                c'64
                c'64
                c'64
                c'64
            }
        }
        {
            \time 2/16
            c'16
            c'16
        }
    }
    '''

    new = measuretools.fuse_measures(t[:])

    r'''
    {
        \time 19/80
        \scaleDurations #'(4 . 5) {
            c'64
            c'64
            c'64
            c'64
            c'64
            c'64
            c'64
            c'64
            c'64
            c'16 ~
            c'64
            c'16 ~
            c'64
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            {
                \time 19/80
                \scaleDurations #'(4 . 5) {
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'64
                    c'16 ~
                    c'64
                    c'16 ~
                    c'64
                }
            }
        }
        '''
        )
