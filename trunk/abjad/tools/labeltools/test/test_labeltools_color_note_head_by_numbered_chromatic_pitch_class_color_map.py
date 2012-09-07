from abjad import *


def test_labeltools_color_note_head_by_numbered_chromatic_pitch_class_color_map_01():

    t = Note(12, (1, 4))
    labeltools.color_note_head_by_numbered_chromatic_pitch_class_color_map(t)

    r'''
    \once \override NoteHead #'color = #(x11-color 'red)
    c''4
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\once \\override NoteHead #'color = #(x11-color 'red)\nc''4"
