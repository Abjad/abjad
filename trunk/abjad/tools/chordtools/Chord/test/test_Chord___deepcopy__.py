# -*- encoding: utf-8 -*-
from abjad import *
import copy


def test_Chord___deepcopy___01():
    r'''Chord deepchopies note heads.
    '''

    chord_1 = Chord("<c' e' g'>4")
    chord_1[0].tweak.color = 'red'
    chord_2 = copy.deepcopy(chord_1)

    assert testtools.compare(
        chord_1,
        r'''
        <
            \tweak #'color #red
            c'
            e'
            g'
        >4
        '''
        )

    assert testtools.compare(
        chord_2,
        r'''
        <
            \tweak #'color #red
            c'
            e'
            g'
        >4
        '''
        )

    assert chord_2[0]._client is chord_2
    assert chord_2[1]._client is chord_2
    assert chord_2[2]._client is chord_2

    assert chord_1.lilypond_format == chord_2.lilypond_format
    assert chord_1 is not chord_2

    assert chord_1[0] == chord_2[0]
    assert chord_1[1] == chord_2[1]
    assert chord_1[2] == chord_2[2]

    assert chord_1[0] is not chord_2[0]
    assert chord_1[1] is not chord_2[1]
    assert chord_1[2] is not chord_2[2]
