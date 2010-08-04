from abjad import *
import py.test


def test_PitchClass___init____01( ):
   '''Pitch class initialization works with numbers.'''

   pc = pitchtools.PitchClass(0)
   assert pc.number == 0

   pc = pitchtools.PitchClass(0.5)
   assert pc.number == 0.5

   pc = pitchtools.PitchClass(1)
   assert pc.number == 1

   pc = pitchtools.PitchClass(1.5)
   assert pc.number == 1.5

   pc = pitchtools.PitchClass(13)
   assert pc.number == 1

   pc = pitchtools.PitchClass(13.5)
   assert pc.number == 1.5


def test_PitchClass___init____02( ):
   '''Pitch class initialization works with other pitch classes.'''

   pc = pitchtools.PitchClass(pitchtools.PitchClass(0))
   assert pc.number == 0

   pc = pitchtools.PitchClass(pitchtools.PitchClass(12))
   assert pc.number == 0


def test_PitchClass___init____03( ):
   '''PitchClass initialization works with pitches.'''

   pc = pitchtools.PitchClass(pitchtools.NamedPitch(0))
   assert pc.number == 0

   pc = pitchtools.PitchClass(pitchtools.NamedPitch(12))
   assert pc.number == 0


def test_PitchClass___init____04( ):
   '''Pitch class initialization works with notes.'''

   note = Note(13, (1, 4))
   pc = pitchtools.PitchClass(note)
   assert pc == pitchtools.PitchClass(1)


def test_PitchClass___init____05( ):
   '''Pitch class initialization works with one-note chords.'''

   chord = Chord([13], (1, 4))
   pc = pitchtools.PitchClass(chord)
   assert pc == pitchtools.PitchClass(1)


def test_PitchClass___init____06( ):
   '''Init with named pitch class instance.'''

   npc = pitchtools.NamedPitchClass('cs')
   pc = pitchtools.PitchClass(npc)
   assert pc == pitchtools.PitchClass(1)


def test_PitchClass___init____07( ):
   '''PitchClass initialization raises ValueError.'''

   assert py.test.raises(ValueError, "pitchtools.PitchClass('foo')")


def test_PitchClass___init____08( ):
   '''PitchClass initialization raises TypeError on rest.'''

   rest = Rest((1, 4))
   assert py.test.raises(TypeError, 'pitchtools.PitchClass(rest)')


def test_PitchClass___init____09( ):
   '''PitchClass initialization raises MissingPitchError on empty chord.''' 

   chord = Chord([ ], (1, 4))
   assert py.test.raises(MissingPitchError, 'pitchtools.PitchClass(chord)')


def test_PitchClass___init____10( ):
   '''Init from named pitch class string.'''

   assert pitchtools.PitchClass('c').number == 0
   assert pitchtools.PitchClass('cs').number == 1
   assert pitchtools.PitchClass('cf').number == 11
   assert pitchtools.PitchClass('css').number == 2
