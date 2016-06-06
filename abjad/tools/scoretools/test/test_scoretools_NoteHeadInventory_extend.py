# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_NoteHeadInventory_extend_01():
    r'''Extend chord with tweaked note heads.
    '''

    chord = Chord("<ef'>4")
    note_heads = []
    note_head = scoretools.NoteHead("cs''")
    note_head.tweak.color = 'blue'
    note_heads.append(note_head)
    note_head = scoretools.NoteHead("f''")
    note_head.tweak.color = 'green'
    note_heads.append(note_head)
    chord.note_heads.extend(note_heads)

    assert format(chord) == stringtools.normalize(
        r'''
        <
            ef'
            \tweak color #blue
            cs''
            \tweak color #green
            f''
        >4
        '''
        )

    assert inspect_(chord).is_well_formed()
