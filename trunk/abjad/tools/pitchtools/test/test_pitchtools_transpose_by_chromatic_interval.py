from abjad import *


def test_pitchtools_transpose_by_chromatic_interval_01( ):
   '''Transpose pitch.'''

   pitch = Pitch(12)
   interval = pitchtools.ChromaticInterval(-3)
   new = pitchtools.transpose_by_chromatic_interval(pitch, interval)
   assert new == Pitch(9)
   assert new is not pitch


def test_pitchtools_transpose_by_chromatic_interval_02( ):
   '''Transpose note.'''

   note = Note(12, (1, 4))
   interval = pitchtools.ChromaticInterval(-3)
   new = pitchtools.transpose_by_chromatic_interval(note, interval)
   assert new.pitch == Pitch(9)
   assert new is not note


def test_pitchtools_transpose_by_chromatic_interval_03( ):
   '''Transpose chord.'''

   chord = Chord([12, 13, 14], (1, 4))
   interval = pitchtools.ChromaticInterval(-3)
   new = pitchtools.transpose_by_chromatic_interval(chord, interval)
   assert new.pitches == tuple([Pitch(x) for x in [9, 10, 11]])
   assert new is not chord
