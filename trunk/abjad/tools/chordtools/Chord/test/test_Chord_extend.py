# -*- encoding: utf-8 -*-
from abjad import *


def test_Chord_extend_01():
    r'''Extend chord with tweaked note heads.
    '''

    chord = Chord("<ef'>4")
    note_heads = []
    note_head = notetools.NoteHead("cs''")
    note_head.tweak.color = 'blue'
    note_heads.append(note_head)
    note_head = notetools.NoteHead("f''")
    note_head.tweak.color = 'green'
    note_heads.append(note_head)
    chord.extend(note_heads)

    assert testtools.compare(
        chord,
        r'''
        <
            ef'
            \tweak #'color #blue
            cs''
            \tweak #'color #green
            f''
        >4
        '''
        )

    assert inspect(chord).is_well_formed()
