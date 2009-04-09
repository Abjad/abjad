from abjad import *


def test_chord_arpeggiate_01( ):
   '''Returns list of notes with pitches equal to those in chord.'''

   t = Chord([0, 2, 9], (1, 4))
   notes = chordtools.arpeggiate(t)

   "[Note(c', 4), Note(d', 4), Note(a', 4)]"

   for note, pitch in zip(notes, t.pitches):
      assert note.pitch == pitch
      assert note.duration.written == t.duration.written
