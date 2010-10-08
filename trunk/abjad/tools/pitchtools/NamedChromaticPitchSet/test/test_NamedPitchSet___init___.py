from abjad import *


def test_NamedPitchSet___init____01( ):
   '''Works with numbers.'''

   assert len(pitchtools.NamedChromaticPitchSet([12, 14, 18, 19])) == 4


def test_NamedPitchSet___init____02( ):
   '''Works with pitches.'''

   assert len(pitchtools.NamedChromaticPitchSet([pitchtools.NamedChromaticPitch(x) for x in [12, 14, 18, 19]])) == 4


def test_NamedPitchSet___init____03( ):
   '''Works with notes.'''

   note = Note(13, (1, 4))
   pitch_set = pitchtools.NamedChromaticPitchSet(pitchtools.list_named_chromatic_pitches_in_expr(note))
   assert len(pitch_set) == 1


def test_NamedPitchSet___init____04( ):
   '''Works with chords.'''

   chord = Chord([13, 14, 15], (1, 4))
   pitch_set = pitchtools.NamedChromaticPitchSet(pitchtools.list_named_chromatic_pitches_in_expr(chord))
   assert len(pitch_set) == 3


def test_NamedPitchSet___init____05( ):
   '''Works with chords with duplicate pitches.'''

   chord = Chord([13, 13, 13, 14], (1, 4))
   pitch_set = pitchtools.NamedChromaticPitchSet(pitchtools.list_named_chromatic_pitches_in_expr(chord))
   assert len(pitch_set) == 2


def test_NamedPitchSet___init____06( ):
   '''Works with empty chords.'''

   chord = Chord([ ], (1, 4))
   pitch_set = pitchtools.NamedChromaticPitchSet(pitchtools.list_named_chromatic_pitches_in_expr(chord))
   assert len(pitch_set) == 0


def test_NamedPitchSet___init____07( ):
   '''Works with chords.'''

   assert len(pitchtools.NamedChromaticPitchSet(Chord([12, 14, 18, 19], (1, 4)))) == 4
