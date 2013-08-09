# -*- encoding: utf-8 -*-
from abjad import *


def test_componenttools_copy_components_and_fracture_crossing_spanners_01():
    r'''Deep copy components in 'components'.
    Deep copy spanners that attach to any component in 'components'.
    Fracture spanners that attach to components not in 'components'.
    Return Python list of copied components.'''

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    slur = spannertools.SlurSpanner(voice[:])
    trill = spannertools.TrillSpanner(voice.select_leaves())
    beam = spannertools.BeamSpanner(voice[0][:] + voice[1:2] + voice[2][:])

    r'''
    \new Voice {
        \time 2/8
        c'8 [ ( \startTrillSpan
        d'8
        \time 2/8
        e'8
        f'8
        \time 2/8
        g'8
        a'8 ] ) \stopTrillSpan
    }
    '''

    result = componenttools.copy_components_and_fracture_crossing_spanners(voice.select_leaves()[2:4])
    new = Voice(result)

    r'''
    \new Voice {
        e'8 \startTrillSpan
        f'8 \stopTrillSpan
    }
    '''

    assert select(voice).is_well_formed()
    assert select(new).is_well_formed()
    assert testtools.compare(
        new,
        r'''
        \new Voice {
            e'8 \startTrillSpan
            f'8 \stopTrillSpan
        }
        '''
        )


def test_componenttools_copy_components_and_fracture_crossing_spanners_02():
    r'''Copy one measure and fracture spanners.
    '''

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    slur = spannertools.SlurSpanner(voice[:])
    trill = spannertools.TrillSpanner(voice.select_leaves())
    beam = spannertools.BeamSpanner(voice[0][:] + voice[1:2] + voice[2][:])

    r'''
    \new Voice {
        {
            \time 2/8
            c'8 [ ( \startTrillSpan
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
            a'8 ] ) \stopTrillSpan
        }
    }
    '''

    result = componenttools.copy_components_and_fracture_crossing_spanners(voice[1:2])
    new = Voice(result)

    r'''
    \new Voice {
        {
            \time 2/8
            e'8 [ ( \startTrillSpan
            f'8 ] ) \stopTrillSpan
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert select(new).is_well_formed()
    assert testtools.compare(
        new,
        r'''
        \new Voice {
            {
                \time 2/8
                e'8 [ ( \startTrillSpan
                f'8 ] ) \stopTrillSpan
            }
        }
        '''
        )


def test_componenttools_copy_components_and_fracture_crossing_spanners_03():
    r'''Three notes crossing measure boundaries.
    '''

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    slur = spannertools.SlurSpanner(voice[:])
    trill = spannertools.TrillSpanner(voice.select_leaves())
    beam = spannertools.BeamSpanner(voice[0][:] + voice[1:2] + voice[2][:])

    r'''
    \new Voice {
        {
            \time 2/8
            c'8 [ ( \startTrillSpan
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
            a'8 ] ) \stopTrillSpan
        }
    }
    '''

    result = componenttools.copy_components_and_fracture_crossing_spanners(voice.select_leaves()[-3:])
    new = Voice(result)

    r'''
    \new Voice {
        f'8 \startTrillSpan
        g'8 [
        a'8 ] \stopTrillSpan
    }
    '''

    assert select(voice).is_well_formed()
    assert select(new).is_well_formed()
    assert testtools.compare(
        new,
        r'''
        \new Voice {
            f'8 \startTrillSpan
            g'8 [
            a'8 ] \stopTrillSpan
        }
        '''
        )


def test_componenttools_copy_components_and_fracture_crossing_spanners_04():
    r'''Optional 'n' argument for multiple copies.
    '''

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    slur = spannertools.SlurSpanner(voice[:])
    trill = spannertools.TrillSpanner(voice.select_leaves())
    beam = spannertools.BeamSpanner(voice[0][:] + voice[1:2] + voice[2][:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    r'''
    \new Voice {
        {
            \time 2/8
            c'8 [ ( \startTrillSpan
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
            a'8 ] ) \stopTrillSpan
        }
    }
    '''

    result = componenttools.copy_components_and_fracture_crossing_spanners(voice[1:2], 3)
    new = Voice(result)
    measuretools.set_always_format_time_signature_of_measures_in_expr(new)

    r'''
    \new Voice {
        {
            \time 2/8
            e'8 [ ( \startTrillSpan
            f'8 ] ) \stopTrillSpan
        }
        {
            \time 2/8
            e'8 [ ( \startTrillSpan
            f'8 ] ) \stopTrillSpan
        }
        {
            \time 2/8
            e'8 [ ( \startTrillSpan
            f'8 ] ) \stopTrillSpan
        }
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        new,
        r'''
        \new Voice {
            {
                \time 2/8
                e'8 [ ( \startTrillSpan
                f'8 ] ) \stopTrillSpan
            }
            {
                \time 2/8
                e'8 [ ( \startTrillSpan
                f'8 ] ) \stopTrillSpan
            }
            {
                \time 2/8
                e'8 [ ( \startTrillSpan
                f'8 ] ) \stopTrillSpan
            }
        }
        '''
        )
