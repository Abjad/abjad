# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_list_named_pitches_in_expr_01():
    r'''Works with containers.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    named_pitches = pitchtools.list_named_pitches_in_expr(tuplet)

    assert named_pitches == (
        NamedPitch('c', 4),
        NamedPitch('d', 4),
        NamedPitch('e', 4),
        )


def test_pitchtools_list_named_pitches_in_expr_02():
    r'''Works with spanners.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, staff[:])
    named_pitches = pitchtools.list_named_pitches_in_expr(beam)

    assert named_pitches == (
        NamedPitch('c', 4),
        NamedPitch('d', 4),
        NamedPitch('e', 4),
        NamedPitch('f', 4),
        )


def test_pitchtools_list_named_pitches_in_expr_03():
    r'''Works with pitch sets.
    '''

    pitch_set = pitchtools.PitchSet([0, 2, 4, 5])
    named_pitches = pitchtools.list_named_pitches_in_expr(pitch_set)

    assert named_pitches == (
        NamedPitch('c', 4),
        NamedPitch('d', 4),
        NamedPitch('e', 4),
        NamedPitch('f', 4),
        )


def test_pitchtools_list_named_pitches_in_expr_04():
    r'''Works with pitch arrays.
    '''

    array = pitchtools.PitchArray([
        [1, (2, 1), (-1.5, 2)],
        [(7, 2), (6, 1), 1],
        ])

    assert pitchtools.list_named_pitches_in_expr(array) == (
        NamedPitch('d', 4),
        NamedPitch('bqf', 3),
        NamedPitch('g', 4),
        NamedPitch('fs', 4),
        )


def test_pitchtools_list_named_pitches_in_expr_05():
    r'''Works with list or tuple of pitches.
    '''

    named_pitches = (
        NamedPitch(0),
        Note(2, (1, 4)),
        Chord([4, 6, 7], (1, 4)),
        )
    assert pitchtools.list_named_pitches_in_expr(named_pitches) == (
        NamedPitch('c', 4),
        NamedPitch('d', 4),
        NamedPitch('e', 4),
        NamedPitch('fs', 4),
        NamedPitch('g', 4),
        )
