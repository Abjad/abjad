# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_NoteHeadInventory_append_01():
    r'''Append tweaked note head to chord.
    '''

    chord = Chord("<c' d'>4")
    note_head = scoretools.NoteHead("b'")
    note_head.tweak.style = 'harmonic'
    chord.note_heads.append(note_head)

    assert format(chord) == stringtools.normalize(
        r'''
        <
            c'
            d'
            \tweak style #'harmonic
            b'
        >4
        '''
        )

    assert note_head._client is chord
