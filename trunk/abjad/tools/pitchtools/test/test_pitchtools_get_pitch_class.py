from abjad import *
import py.test


def test_pitchtools_get_pitch_class_01( ):
   '''Works on notes.'''

   note = Note(13, (1, 4))
   assert pitchtools.get_pitch_class(note) == pitchtools.PitchClass(1)


def test_pitchtools_get_pitch_class_02( ):
   '''Works on one-note chords.'''

   chord = Chord([13], (1, 4))
   assert pitchtools.get_pitch_class(chord) == pitchtools.PitchClass(1)


def test_pitchtools_get_pitch_class_03( ):
   '''Raises exception on empty chord.'''

   chord = Chord([ ], (1, 4))
   assert py.test.raises(MissingPitchError, 
      'pitchtools.get_pitch_class(chord)')


def test_pitchtools_get_pitch_class_04( ):
   '''Raises exception on multiple-note chord.'''

   chord = Chord([13, 14, 15], (1, 4))
   assert py.test.raises(ExtraPitchError, 
      'pitchtools.get_pitch_class(chord)')
