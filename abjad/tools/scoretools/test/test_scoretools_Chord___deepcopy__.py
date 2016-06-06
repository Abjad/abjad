# -*- coding: utf-8 -*-
from abjad import *
import copy


def test_scoretools_Chord___deepcopy___01():
    r'''Chord deepchopies note heads.
    '''

    chord_1 = Chord("<c' e' g'>4")
    chord_1.note_heads[0].tweak.color = 'red'
    chord_2 = copy.deepcopy(chord_1)

    assert format(chord_1) == stringtools.normalize(
        r'''
        <
            \tweak color #red
            c'
            e'
            g'
        >4
        '''
        )

    assert format(chord_2) == stringtools.normalize(
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
