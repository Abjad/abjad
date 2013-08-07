# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import pitcharraytools


def test_pitchtools_list_named_chromatic_pitches_in_expr_01():
    r'''Works with containers.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    namedchromaticpitch = pitchtools.list_named_chromatic_pitches_in_expr(tuplet)

    assert namedchromaticpitch == (pitchtools.NamedChromaticPitch('c', 4), pitchtools.NamedChromaticPitch('d', 4), pitchtools.NamedChromaticPitch('e', 4))


def test_pitchtools_list_named_chromatic_pitches_in_expr_02():
    r'''Works with spanners.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff[:])
    namedchromaticpitch = pitchtools.list_named_chromatic_pitches_in_expr(beam)

    assert namedchromaticpitch == (pitchtools.NamedChromaticPitch('c', 4), pitchtools.NamedChromaticPitch('d', 4), pitchtools.NamedChromaticPitch('e', 4), pitchtools.NamedChromaticPitch('f', 4))


def test_pitchtools_list_named_chromatic_pitches_in_expr_03():
    r'''Works with pitch sets.
    '''

    pitch_set = pitchtools.NamedChromaticPitchSet([0, 2, 4, 5])
    namedchromaticpitch = pitchtools.list_named_chromatic_pitches_in_expr(pitch_set)

    assert namedchromaticpitch == (pitchtools.NamedChromaticPitch('c', 4), pitchtools.NamedChromaticPitch('d', 4), pitchtools.NamedChromaticPitch('e', 4), pitchtools.NamedChromaticPitch('f', 4))


def test_pitchtools_list_named_chromatic_pitches_in_expr_04():
    r'''Works with pitch arrays.
    '''

    array = pitcharraytools.PitchArray([
        [1, (2, 1), (-1.5, 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bqf     ]
    [g'      ] [fs'] []
    '''

    assert pitchtools.list_named_chromatic_pitches_in_expr(array) == (
        pitchtools.NamedChromaticPitch('d', 4), pitchtools.NamedChromaticPitch('bqf', 3), pitchtools.NamedChromaticPitch('g', 4), pitchtools.NamedChromaticPitch('fs', 4))


def test_pitchtools_list_named_chromatic_pitches_in_expr_05():
    r'''Works with list or tuple of pitches.
    '''

    namedchromaticpitch = [pitchtools.NamedChromaticPitch(0), Note(2, (1, 4)), Chord([4, 6, 7], (1, 4))]
    assert pitchtools.list_named_chromatic_pitches_in_expr(namedchromaticpitch) == (pitchtools.NamedChromaticPitch('c', 4), pitchtools.NamedChromaticPitch('d', 4), pitchtools.NamedChromaticPitch('e', 4), pitchtools.NamedChromaticPitch('fs', 4), pitchtools.NamedChromaticPitch('g', 4))
