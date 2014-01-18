# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_color_chord_note_heads_by_numbered_pitch_class_01():
    r'''Works on chords.
    '''

    pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
    colors = ['red', 'blue', 'green']
    color_map = pitchtools.NumberedPitchClassColorMap(pitches, colors)

    chord = Chord([12, 14, 18, 21, 23], (1, 4))
    labeltools.color_chord_note_heads_in_expr_by_pitch_class_color_map(
        chord, color_map)

    assert systemtools.TestManager.compare(
        chord,
        r'''
        <
            \tweak #'color #red
            c''
            \tweak #'color #red
            d''
            \tweak #'color #green
            fs''
            \tweak #'color #green
            a''
            \tweak #'color #blue
            b''
        >4
        '''
        )

    assert inspect_(chord).is_well_formed()


def test_labeltools_color_chord_note_heads_by_numbered_pitch_class_02():
    r'''Works on notes.
    '''

    pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
    colors = ['red', 'blue', 'green']
    color_map = pitchtools.NumberedPitchClassColorMap(pitches, colors)

    note = Note("c'4")
    labeltools.color_chord_note_heads_in_expr_by_pitch_class_color_map(
        note, color_map)

    assert systemtools.TestManager.compare(
        note,
        r'''
        \once \override NoteHead #'color = #red
        c'4
        '''
        )

    assert inspect_(note).is_well_formed()
