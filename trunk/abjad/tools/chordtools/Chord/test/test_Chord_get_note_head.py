from abjad import *
import py.test


def test_Chord_get_note_head_01():
    '''Get note head.
    '''

    chord = Chord([0, 2, 11], Duration(1, 4))

    note_head = chord.get_note_head(0)
    assert note_head.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 0

    note_head = chord.get_note_head(2)
    assert note_head.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 2

    note_head = chord.get_note_head(11)
    assert note_head.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 11


def test_Chord_get_note_head_02():
    '''Exceptions.
    '''

    chord = Chord([0, 2, 2], Duration(1, 4))

    assert py.test.raises(MissingNoteHeadError, 'chord.get_note_head(9)')
    assert py.test.raises(ExtraNoteHeadError, 'chord.get_note_head(2)')
