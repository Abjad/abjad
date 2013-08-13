# -*- encoding: utf-8 -*-
from abjad import *


def test_ContiguousSelection_copy_and_fracture_crossing_spanners_01():
    r'''Deep copy components in 'components'.
    Deep copy spanners that attach to any component in 'components'.
    Fracture spanners that attach to components not in 'components'.
    Return Python list of copied components.'''

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    slur = spannertools.SlurSpanner(voice[:])
    trill = spannertools.TrillSpanner(voice.select_leaves())
    beam = spannertools.BeamSpanner(voice[0][:] + voice[1:2] + voice[2][:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ ( \startTrillSpan
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ] ) \stopTrillSpan
            }
        }
        '''
        )

    selection = voice.select_leaves()[2:4]
    result = selection.copy_and_fracture_crossing_spanners()
    new = Voice(result)

    assert testtools.compare(
        new,
        r'''
        \new Voice {
            e'8 \startTrillSpan
            f'8 \stopTrillSpan
        }
        '''
        )
    assert select(voice).is_well_formed()
    assert select(new).is_well_formed()


def test_ContiguousSelection_copy_and_fracture_crossing_spanners_02():
    r'''Copy one measure and fracture spanners.
    '''

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    slur = spannertools.SlurSpanner(voice[:])
    trill = spannertools.TrillSpanner(voice.select_leaves())
    beam = spannertools.BeamSpanner(voice[0][:] + voice[1:2] + voice[2][:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ ( \startTrillSpan
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ] ) \stopTrillSpan
            }
        }
        '''
        )

    result = voice[1:2].copy_and_fracture_crossing_spanners()
    new = Voice(result)

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
    assert select(voice).is_well_formed()
    assert select(new).is_well_formed()


def test_ContiguousSelection_copy_and_fracture_crossing_spanners_03():
    r'''Three notes crossing measure boundaries.
    '''

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    slur = spannertools.SlurSpanner(voice[:])
    trill = spannertools.TrillSpanner(voice.select_leaves())
    beam = spannertools.BeamSpanner(voice[0][:] + voice[1:2] + voice[2][:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 2/8
                c'8 [ ( \startTrillSpan
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ] ) \stopTrillSpan
            }
        }
        '''
        )

    selection = voice.select_leaves()[-3:]
    result = selection.copy_and_fracture_crossing_spanners()
    new = Voice(result)

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
    assert select(voice).is_well_formed()
    assert select(new).is_well_formed()


def test_ContiguousSelection_copy_and_fracture_crossing_spanners_04():
    r'''Optional 'n' argument for multiple copies.
    '''

    voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    slur = spannertools.SlurSpanner(voice[:])
    trill = spannertools.TrillSpanner(voice.select_leaves())
    beam = spannertools.BeamSpanner(voice[0][:] + voice[1:2] + voice[2][:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(voice)

    assert testtools.compare(
        voice,
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
        )

    result = voice[1:2].copy_and_fracture_crossing_spanners(n=3)
    new = Voice(result)
    measuretools.set_always_format_time_signature_of_measures_in_expr(new)

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
    assert select(voice).is_well_formed()


def test_ContiguousSelection_copy_and_fracture_crossing_spanners_05():

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
    new_selection = selection.copy_and_fracture_crossing_spanners()
    new_voice = new_selection[0]
    spannertools.detach_spanners_attached_to_components_in_expr(new_voice)
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


def test_ContiguousSelection_copy_and_fracture_crossing_spanners_06():

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

    result = voice[1:].copy_and_fracture_crossing_spanners()
    new_voice = Voice(result)
    spannertools.detach_spanners_attached_to_components_in_expr(new_voice)
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


def test_ContiguousSelection_copy_and_fracture_crossing_spanners_07():

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

    result = voice.select_leaves()[:6].copy_and_fracture_crossing_spanners()
    new_voice = Voice(result)
    spannertools.detach_spanners_attached_to_components_in_expr(new_voice)
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


def test_ContiguousSelection_copy_and_fracture_crossing_spanners_08():

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

    result = voice[-2:].copy_and_fracture_crossing_spanners()
    new_voice = Voice(result)
    spannertools.detach_spanners_attached_to_components_in_expr(new_voice)
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


def test_ContiguousSelection_copy_and_fracture_crossing_spanners_09():

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

    result = voice[-2:].copy_and_fracture_crossing_spanners(n=3)
    new_voice = Voice(result)
    spannertools.detach_spanners_attached_to_components_in_expr(new_voice)
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


def test_ContiguousSelection_copy_and_fracture_crossing_spanners_10():
    r'''Copies hairpin.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.CrescendoSpanner(staff[:4])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 \<
            cs'8
            d'8
            ef'8 \!
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    new_notes = staff[:4].copy_and_fracture_crossing_spanners()
    staff.extend(new_notes)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 \<
            cs'8
            d'8
            ef'8 \!
            e'8
            f'8
            fs'8
            g'8
            c'8 \<
            cs'8
            d'8
            ef'8 \!
        }
        '''
        )
    assert select(staff).is_well_formed()
