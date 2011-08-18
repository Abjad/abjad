from abjad import *


def test_chordtools_color_chord_note_heads_by_numeric_pitch_class_01():
    '''Works on chords.'''

    pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]] 
    colors = ['red', 'blue', 'green']
    color_map = pitchtools.NumberedChromaticPitchClassColorMap(pitches, colors)

    chord = Chord([12, 14, 18, 21, 23], (1, 4))
    chordtools.color_chord_note_heads_by_pitch_class_color_map(chord, color_map)

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

    assert componenttools.is_well_formed_component(chord)
    assert chord.format == "<\n\t\\tweak #'color #red\n\tc''\n\t\\tweak #'color #red\n\td''\n\t\\tweak #'color #green\n\tfs''\n\t\\tweak #'color #green\n\ta''\n\t\\tweak #'color #blue\n\tb''\n>4"


def test_chordtools_color_chord_note_heads_by_numeric_pitch_class_02():
    '''Works on notes.'''

    pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]] 
    colors = ['red', 'blue', 'green']
    color_map = pitchtools.NumberedChromaticPitchClassColorMap(pitches, colors)

    note = Note("c'4")
    chordtools.color_chord_note_heads_by_pitch_class_color_map(note, color_map)

    r'''
    \once \override NoteHead #'color = #red
    c'4
    '''

    assert componenttools.is_well_formed_component(note)
    assert note.format == "\\once \\override NoteHead #'color = #red\nc'4"
