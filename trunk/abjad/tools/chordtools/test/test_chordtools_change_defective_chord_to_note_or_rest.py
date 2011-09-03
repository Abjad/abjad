from abjad import *


def test_chordtools_change_defective_chord_to_note_or_rest_01():
    '''Change zero-length chord as rest.'''

    t = Chord([], (1, 8))
    rest = chordtools.change_defective_chord_to_note_or_rest(t)

    assert isinstance(t, Chord)
    assert isinstance(rest, Rest)


def test_chordtools_change_defective_chord_to_note_or_rest_02():
    '''Change length-one chord as note.'''

    t = Chord([0], (1, 8))
    note = chordtools.change_defective_chord_to_note_or_rest(t)

    assert isinstance(t, Chord)
    assert isinstance(note, Note)


def test_chordtools_change_defective_chord_to_note_or_rest_03():
    '''Return notes and rests unchanged.'''

    note = Note("c'4")
    assert chordtools.change_defective_chord_to_note_or_rest(note) is note

    rest = Rest((1, 4))
    assert chordtools.change_defective_chord_to_note_or_rest(rest) is rest
