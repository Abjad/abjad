from abjad import *
import py.test


def test_chordtools_get_note_head_from_chord_by_pitch_01():
    '''Return reference to note_head in chord with pitch equal to pitch.'''

    chord = Chord([0, 2, 11], Duration(1, 4))

    note_head = chordtools.get_note_head_from_chord_by_pitch(chord, 0)
    assert note_head.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 0

    note_head = chordtools.get_note_head_from_chord_by_pitch(chord, 2)
    assert note_head.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 2

    note_head = chordtools.get_note_head_from_chord_by_pitch(chord, 11)
    assert note_head.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 11


def test_chordtools_get_note_head_from_chord_by_pitch_02():
    '''Raise MissingNoteHeadError and ExtraNoteHeadError as required.'''

    chord = Chord([0, 2, 2], Duration(1, 4))

    assert py.test.raises(
        MissingNoteHeadError, 'chordtools.get_note_head_from_chord_by_pitch(chord, 9)')

    assert py.test.raises(
        ExtraNoteHeadError, 'chordtools.get_note_head_from_chord_by_pitch(chord, 2)')
