from abjad import *
import py.test


def test_PitchClass___init____01( ):
   '''Pitch class initialization works with numbers.'''

   pc = pitchtools.NumericPitchClass(0)
   assert pc.number == 0

   pc = pitchtools.NumericPitchClass(0.5)
   assert pc.number == 0.5

   pc = pitchtools.NumericPitchClass(1)
   assert pc.number == 1

   pc = pitchtools.NumericPitchClass(1.5)
   assert pc.number == 1.5

   pc = pitchtools.NumericPitchClass(13)
   assert pc.number == 1

   pc = pitchtools.NumericPitchClass(13.5)
   assert pc.number == 1.5


def test_PitchClass___init____02( ):
   '''Pitch class initialization works with other pitch classes.'''

   pc = pitchtools.NumericPitchClass(pitchtools.NumericPitchClass(0))
   assert pc.number == 0

   pc = pitchtools.NumericPitchClass(pitchtools.NumericPitchClass(12))
   assert pc.number == 0


def test_PitchClass___init____03( ):
   '''PitchClass initialization works with pitches.'''

   pc = pitchtools.NumericPitchClass(pitchtools.NamedPitch(0))
   assert pc.number == 0

   pc = pitchtools.NumericPitchClass(pitchtools.NamedPitch(12))
   assert pc.number == 0


def test_PitchClass___init____04( ):
   '''Pitch class initialization works with notes.'''

   note = Note(13, (1, 4))
   pc = pitchtools.NumericPitchClass(note)
   assert pc == pitchtools.NumericPitchClass(1)


def test_PitchClass___init____05( ):
   '''Pitch class initialization works with one-note chords.'''

   chord = Chord([13], (1, 4))
   pc = pitchtools.NumericPitchClass(chord)
   assert pc == pitchtools.NumericPitchClass(1)


def test_PitchClass___init____06( ):
   '''Init with named pitch class instance.'''

   npc = pitchtools.NamedPitchClass('cs')
   pc = pitchtools.NumericPitchClass(npc)
   assert pc == pitchtools.NumericPitchClass(1)


def test_PitchClass___init____07( ):
   '''PitchClass initialization raises ValueError.'''

   assert py.test.raises(ValueError, "pitchtools.NumericPitchClass('foo')")


def test_PitchClass___init____08( ):
   '''PitchClass initialization raises TypeError on rest.'''

   rest = Rest((1, 4))
   assert py.test.raises(TypeError, 'pitchtools.NumericPitchClass(rest)')


def test_PitchClass___init____09( ):
   '''PitchClass initialization raises MissingPitchError on empty chord.''' 

   chord = Chord([ ], (1, 4))
   assert py.test.raises(MissingPitchError, 'pitchtools.NumericPitchClass(chord)')


def test_PitchClass___init____10( ):
   '''Init from named pitch class string.'''

   assert pitchtools.NumericPitchClass('c').number == 0
   assert pitchtools.NumericPitchClass('cs').number == 1
   assert pitchtools.NumericPitchClass('cf').number == 11
   assert pitchtools.NumericPitchClass('css').number == 2
