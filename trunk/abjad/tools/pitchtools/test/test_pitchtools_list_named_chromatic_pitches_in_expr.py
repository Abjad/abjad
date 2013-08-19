# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import pitcharraytools


def test_pitchtools_list_named_chromatic_pitches_in_expr_01():
    r'''Works with containers.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    namedchromaticpitch = pitchtools.list_named_chromatic_pitches_in_expr(tuplet)

    assert namedchromaticpitch == (pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('e', 4))


def test_pitchtools_list_named_chromatic_pitches_in_expr_02():
    r'''Works with spanners.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff[:])
    namedchromaticpitch = pitchtools.list_named_chromatic_pitches_in_expr(beam)

    assert namedchromaticpitch == (pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('e', 4), pitchtools.NamedPitch('f', 4))


def test_pitchtools_list_named_chromatic_pitches_in_expr_03():
    r'''Works with pitch sets.
    '''

    pitch_set = pitchtools.NamedPitchSet([0, 2, 4, 5])
    namedchromaticpitch = pitchtools.list_named_chromatic_pitches_in_expr(pitch_set)

    assert namedchromaticpitch == (pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('e', 4), pitchtools.NamedPitch('f', 4))


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
        pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('bqf', 3), pitchtools.NamedPitch('g', 4), pitchtools.NamedPitch('fs', 4))


def test_pitchtools_list_named_chromatic_pitches_in_expr_05():
    r'''Works with list or tuple of pitches.
    '''

    namedchromaticpitch = [pitchtools.NamedPitch(0), Note(2, (1, 4)), Chord([4, 6, 7], (1, 4))]
    assert pitchtools.list_named_chromatic_pitches_in_expr(namedchromaticpitch) == (pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('e', 4), pitchtools.NamedPitch('fs', 4), pitchtools.NamedPitch('g', 4))
