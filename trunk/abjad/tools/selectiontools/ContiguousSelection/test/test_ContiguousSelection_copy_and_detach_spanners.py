# -*- encoding: utf-8 -*-
from abjad import *


def test_ContiguousSelection_copy_and_detach_spanners_01():

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2] + voice[2][:] + voice[3][:])
    slur = spannertools.SlurSpanner(voice[0][:] + voice[1][:] + voice[2:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    selection = selectiontools.ContiguousSelection(music=voice)
    new_selection = selection.copy_and_detach_spanners()
    new_voice = new_selection[0]
    measuretools.set_always_format_time_signature_of_measures_in_expr(new_voice)

    assert testtools.compare(
        new_voice,
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
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8
            }
        }
        '''
        )
    assert select(new_voice).is_well_formed()


def test_ContiguousSelection_copy_and_detach_spanners_02():

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2] + voice[2][:] + voice[3][:])
    slur = spannertools.SlurSpanner(voice[0][:] + voice[1][:] + voice[2:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    result = voice[1:].copy_and_detach_spanners()
    new_voice = Voice(result)
    measuretools.set_always_format_time_signature_of_measures_in_expr(new_voice)

    assert testtools.compare(
        new_voice,
        r'''
        \new Voice {
            {
                \time 2/8
                e'8
                f'8
            }
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
        '''
        )
    assert select(voice).is_well_formed()
    assert select(new_voice).is_well_formed()


def test_ContiguousSelection_copy_and_detach_spanners_03():

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2] + voice[2][:] + voice[3][:])
    slur = spannertools.SlurSpanner(voice[0][:] + voice[1][:] + voice[2:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    result = voice.select_leaves()[:6].copy_and_detach_spanners()
    new_voice = Voice(result)
    measuretools.set_always_format_time_signature_of_measures_in_expr(new_voice)

    assert testtools.compare(
        new_voice,
        r'''
        \new Voice {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
        '''
        )
    assert select(voice).is_well_formed()
    assert select(new_voice).is_well_formed()


def test_ContiguousSelection_copy_and_detach_spanners_04():

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2] + voice[2][:] + voice[3][:])
    slur = spannertools.SlurSpanner(voice[0][:] + voice[1][:] + voice[2:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    result = voice[-2:].copy_and_detach_spanners()
    new_voice = Voice(result)
    measuretools.set_always_format_time_signature_of_measures_in_expr(new_voice)

    assert testtools.compare(
        new_voice,
        r'''
        \new Voice {
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
        '''
        )

    assert select(voice).is_well_formed()
    assert select(new_voice).is_well_formed()


def test_ContiguousSelection_copy_and_detach_spanners_05():

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:2] + voice[2][:] + voice[3][:])
    slur = spannertools.SlurSpanner(voice[0][:] + voice[1][:] + voice[2:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ (
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 2/8
                b'8
                c''8 ] )
            }
        }
        '''
        )

    result = voice[-2:].copy_and_detach_spanners(n=3)
    new_voice = Voice(result)
    measuretools.set_always_format_time_signature_of_measures_in_expr(new_voice)

    assert testtools.compare(
        new_voice,
        r'''
        \new Voice {
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
        '''
        )
    assert select(new_voice).is_well_formed()
