# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_copy_components_and_covered_spanners_01():
    r'''Withdraw components in 'components' from crossing spanners.
    Preserve spanners covered by 'components'.
    Deep copy 'components'.
    Reapply crossing spanners to 'components'.
    Return copy of 'components' with covered spanners.
    '''

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice.select_leaves()[:4])
    slur = spannertools.SlurSpanner(voice[-2:])

    r'''
    \new Voice {
        {
            \time 2/8
            c'8 [
            d'8
        }
        {
            \time 2/8
            e'8
            f'8 ]
        }
        {
            \time 2/8
            g'8 (
            a'8
        }
        {
            \time 2/8
            b'8
            c''8 )
        }
    }
    '''

    result = componenttools.copy_components_and_covered_spanners(voice.select_leaves())
    new = Voice(result)

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
        g'8
        a'8
        b'8
        c''8
    }
    '''

    assert select(voice).is_well_formed()
    assert select(new).is_well_formed()
    assert testtools.compare(
        new.lilypond_format,
        r'''
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )


def test_componenttools_copy_components_and_covered_spanners_02():

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice.select_leaves()[:4])
    slur = spannertools.SlurSpanner(voice[-2:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    r'''
    \new Voice {
        {
            \time 2/8
            c'8 [
            d'8
        }
        {
            \time 2/8
            e'8
            f'8 ]
        }
        {
            \time 2/8
            g'8 (
            a'8
        }
        {
            \time 2/8
            b'8
            c''8 )
        }
    }
    '''

    result = componenttools.copy_components_and_covered_spanners(voice[-3:])
    new = Voice(result)
    measuretools.set_always_format_time_signature_of_measures_in_expr(new)

    r'''
    \new Voice {
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8 (
            a'8
        }
        {
            \time 2/8
            b'8
            c''8 )
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert select(new).is_well_formed()
    assert testtools.compare(
        new.lilypond_format,
        r'''
        \new Voice {
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8 (
                a'8
            }
            {
                \time 2/8
                b'8
                c''8 )
            }
        }
        '''
        )


def test_componenttools_copy_components_and_covered_spanners_03():
    r'''With optional 'n' argument for multiple copies.
    '''

    t = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beam = spannertools.BeamSpanner(t.select_leaves()[:4])
    slur = spannertools.SlurSpanner(t[-2:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Voice {
        {
            \time 2/8
            c'8 [
            d'8
        }
        {
            \time 2/8
            e'8
            f'8 ]
        }
        {
            \time 2/8
            g'8 (
            a'8
        }
        {
            \time 2/8
            b'8
            c''8 )
        }
    }
    '''

    result = componenttools.copy_components_and_covered_spanners(t[-3:], 2)
    new = Voice(result)
    measuretools.set_always_format_time_signature_of_measures_in_expr(new)

    r'''
    \new Voice {
        {
            \time 2/8
            c'8 [
            d'8
        }
        {
            \time 2/8
            e'8
            f'8 ]
        }
        {
            \time 2/8
            g'8 (
            a'8
        }
        {
            \time 2/8
            b'8
            c''8 )
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
                c'8 [
                d'8
            }
            {
                \time 2/8
                e'8
                f'8 ]
            }
            {
                \time 2/8
                g'8 (
                a'8
            }
            {
                \time 2/8
                b'8
                c''8 )
            }
        }
        '''
        )
