# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_color_chord_note_heads_by_numeric_pitch_class_01():
    r'''Works on chords.
    '''

    pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
    colors = ['red', 'blue', 'green']
    color_map = pitchtools.NumberedChromaticPitchClassColorMap(pitches, colors)

    chord = Chord([12, 14, 18, 21, 23], (1, 4))
    labeltools.color_chord_note_heads_in_expr_by_pitch_class_color_map(chord, color_map)

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

    assert select(chord).is_well_formed()
    assert testtools.compare(
        chord.lilypond_format,
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


def test_labeltools_color_chord_note_heads_by_numeric_pitch_class_02():
    r'''Works on notes.
    '''

    pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
    colors = ['red', 'blue', 'green']
    color_map = pitchtools.NumberedChromaticPitchClassColorMap(pitches, colors)

    note = Note("c'4")
    labeltools.color_chord_note_heads_in_expr_by_pitch_class_color_map(note, color_map)

    r'''
    \once \override NoteHead #'color = #red
    c'4
    '''

    assert select(note).is_well_formed()
    assert testtools.compare(
        note.lilypond_format,
        r'''
        \once \override NoteHead #'color = #red
        c'4
        '''
        )
