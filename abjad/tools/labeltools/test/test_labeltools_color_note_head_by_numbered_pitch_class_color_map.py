# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_color_note_head_by_numbered_pitch_class_color_map_01():

    note = Note(12, (1, 4))
    labeltools.color_note_head_by_numbered_pitch_class_color_map(note)

    assert systemtools.TestManager.compare(
        note,
        r'''
        \once \override NoteHead #'color = #(x11-color 'red)
        c''4
        '''
        )

    assert inspect(note).is_well_formed()
