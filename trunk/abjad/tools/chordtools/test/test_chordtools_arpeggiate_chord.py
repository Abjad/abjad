from abjad import *


def test_chordtools_arpeggiate_chord_01():
    '''Returns list of notes with pitches equal to those in chord.'''

    t = Chord([0, 2, 9], (1, 4))
    notes = chordtools.arpeggiate_chord(t)

    "[Note(c', 4), Note(d', 4), Note(a', 4)]"

    for note, pitch in zip(notes, t.written_pitches):
        assert note.written_pitch == pitch
        assert note.written_duration == t.written_duration
