# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Chord___format___01():
    r'''Format chord with one note head.
    '''

    chord = Chord("<cqs'>4")

    assert str(chord) == "<cqs'>4"
    assert format(chord) == "<cqs'>4"
    assert len(chord.note_heads) == 1
    assert len(chord.written_pitches) == 1


def test_scoretools_Chord___format___02():
    r'''Format chord with LilyPond command.
    '''

    chord = Chord("<d' ef' e'>4")
    command = indicatortools.LilyPondCommand('glissando', 'right')
    attach(command, chord)

    assert format(chord) == "<d' ef' e'>4 \\glissando"


def test_scoretools_Chord___format___03():
    r'''Format tweaked chord with LilyPond command.
    '''

    chord = Chord("<d' ef' e'>4")
    chord.note_heads[0].tweak.color = 'red'
    command = indicatortools.LilyPondCommand('glissando', 'right')
    attach(command, chord)

    assert format(chord) == stringtools.normalize(
        r'''
        <
            \tweak color #red
            d'
            ef'
            e'
        >4 \glissando
        '''
        )

    assert inspect_(chord).is_well_formed()


def test_scoretools_Chord___format___04():
    '''Format tweaked chord.
    '''

    chord = Chord("<d' ef' e'>4")
    chord.note_heads[0].tweak.transparent = True

    assert format(chord) == stringtools.normalize(
        r'''
        <
            \tweak transparent ##t
            d'
            ef'
            e'
        >4
        '''
        )


def test_scoretools_Chord___format___05():
    r'''Formats tweaked chord.
    '''

    chord = Chord("<d' ef' e'>4")
    chord.note_heads[0].tweak.style = 'harmonic'

    assert format(chord) == stringtools.normalize(
        r'''
        <
            \tweak style #'harmonic
            d'
            ef'
            e'
        >4
        '''
        )
