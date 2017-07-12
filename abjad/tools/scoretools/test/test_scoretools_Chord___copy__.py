# -*- coding: utf-8 -*-
import abjad
import copy


def test_scoretools_Chord___copy___01():

    chord_1 = abjad.Chord("<ef' cs'' f''>4")
    chord_2 = copy.copy(chord_1)

    assert isinstance(chord_1, abjad.Chord)
    assert isinstance(chord_2, abjad.Chord)
    assert format(chord_1) == format(chord_2)
    assert chord_1 is not chord_2


def test_scoretools_Chord___copy___02():
    r'''Chord copies LilyPond duration multiplier.
    '''

    chord_1 = abjad.Chord("<ef' cs'' f''>4 * 1/2")
    chord_2 = copy.copy(chord_1)

    assert isinstance(chord_1, abjad.Chord)
    assert isinstance(chord_2, abjad.Chord)
    assert format(chord_1) == format(chord_2)
    assert chord_1 is not chord_2


def test_scoretools_Chord___copy___03():
    r'''Chord copies LilyPond grob abjad.overrides and LilyPond context abjad.settings.
    '''

    chord_1 = abjad.Chord("<ef' cs'' f''>4")
    abjad.override(chord_1).staff.note_head.color = 'red'
    abjad.override(chord_1).accidental.color = 'red'
    abjad.setting(chord_1).tuplet_full_length = True
    chord_2 = copy.copy(chord_1)

    assert isinstance(chord_1, abjad.Chord)
    assert isinstance(chord_2, abjad.Chord)
    assert format(chord_1) == format(chord_2)
    assert chord_1 is not chord_2


def test_scoretools_Chord___copy___04():
    r'''Chord copies tweaked note-heads.
    '''

    chord_1 = abjad.Chord("<c' e' g'>4")
    chord_1.note_heads[0].tweak.color = 'red'
    chord_2 = copy.copy(chord_1)

    assert format(chord_1) == abjad.String.normalize(
        r'''
        <
            \tweak color #red
            c'
            e'
            g'
        >4
        '''
        )

    assert format(chord_2) == abjad.String.normalize(
        r'''
        <
            \tweak color #red
            c'
            e'
            g'
        >4
        '''
        )

    assert chord_2.note_heads[0]._client is chord_2
    assert chord_2.note_heads[1]._client is chord_2
    assert chord_2.note_heads[2]._client is chord_2

    assert format(chord_1) == format(chord_2)
    assert chord_1 is not chord_2

    assert chord_1.note_heads[0] == chord_2.note_heads[0]
    assert chord_1.note_heads[1] == chord_2.note_heads[1]
    assert chord_1.note_heads[2] == chord_2.note_heads[2]

    assert chord_1.note_heads[0] is not chord_2.note_heads[0]
    assert chord_1.note_heads[1] is not chord_2.note_heads[1]
    assert chord_1.note_heads[2] is not chord_2.note_heads[2]


def test_scoretools_Chord___copy___05():
    r'''Chord coipes articulations and markup.
    '''

    chord_1 = abjad.Chord("<ef' cs'' f''>4")
    articulation_1 = abjad.Articulation('staccato')
    abjad.attach(articulation_1, chord_1)
    markup_1 = abjad.Markup('foo', Up)
    abjad.attach(markup_1, chord_1)

    chord_2 = copy.copy(chord_1)

    assert format(chord_1) == format(chord_2)
    assert chord_1 is not chord_2

    articulation_2 = abjad.inspect(chord_2).get_indicators(abjad.Articulation)[0]
    assert articulation_1 == articulation_2
    assert articulation_1 is not articulation_2

    markup_2 = abjad.inspect(chord_2).get_markup()[0]
    assert markup_1 == markup_2
    assert markup_1 is not markup_2
