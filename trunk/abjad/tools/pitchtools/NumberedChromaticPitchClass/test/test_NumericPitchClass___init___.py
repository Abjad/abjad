from abjad import *
import py.test


def test_NumberedChromaticPitchClass___init____01( ):
   '''Pitch class initialization works with numbers.'''

   pc = pitchtools.NumberedChromaticPitchClass(0)
   assert pc.number == 0

   pc = pitchtools.NumberedChromaticPitchClass(0.5)
   assert pc.number == 0.5

   pc = pitchtools.NumberedChromaticPitchClass(1)
   assert pc.number == 1

   pc = pitchtools.NumberedChromaticPitchClass(1.5)
   assert pc.number == 1.5

   pc = pitchtools.NumberedChromaticPitchClass(13)
   assert pc.number == 1

   pc = pitchtools.NumberedChromaticPitchClass(13.5)
   assert pc.number == 1.5


def test_NumberedChromaticPitchClass___init____02( ):
   '''Pitch class initialization works with other pitch classes.'''

   pc = pitchtools.NumberedChromaticPitchClass(pitchtools.NumberedChromaticPitchClass(0))
   assert pc.number == 0

   pc = pitchtools.NumberedChromaticPitchClass(pitchtools.NumberedChromaticPitchClass(12))
   assert pc.number == 0


def test_NumberedChromaticPitchClass___init____03( ):
   '''PitchClass initialization works with pitches.'''

   pc = pitchtools.NumberedChromaticPitchClass(pitchtools.NamedPitch(0))
   assert pc.number == 0

   pc = pitchtools.NumberedChromaticPitchClass(pitchtools.NamedPitch(12))
   assert pc.number == 0


def test_NumberedChromaticPitchClass___init____04( ):
   '''Pitch class initialization works with notes.'''

   note = Note(13, (1, 4))
   pc = pitchtools.NumberedChromaticPitchClass(note)
   assert pc == pitchtools.NumberedChromaticPitchClass(1)


def test_NumberedChromaticPitchClass___init____05( ):
   '''Pitch class initialization works with one-note chords.'''

   chord = Chord([13], (1, 4))
   pc = pitchtools.NumberedChromaticPitchClass(chord)
   assert pc == pitchtools.NumberedChromaticPitchClass(1)


def test_NumberedChromaticPitchClass___init____06( ):
   '''Init with named pitch class instance.'''

   npc = pitchtools.NamedPitchClass('cs')
   pc = pitchtools.NumberedChromaticPitchClass(npc)
   assert pc == pitchtools.NumberedChromaticPitchClass(1)


def test_NumberedChromaticPitchClass___init____07( ):
   '''PitchClass initialization raises ValueError.'''

   assert py.test.raises(ValueError, "pitchtools.NumberedChromaticPitchClass('foo')")


def test_NumberedChromaticPitchClass___init____08( ):
   '''PitchClass initialization raises TypeError on rest.'''

   rest = Rest((1, 4))
   assert py.test.raises(TypeError, 'pitchtools.NumberedChromaticPitchClass(rest)')


def test_NumberedChromaticPitchClass___init____09( ):
   '''PitchClass initialization raises MissingPitchError on empty chord.''' 

   chord = Chord([ ], (1, 4))
   assert py.test.raises(MissingPitchError, 'pitchtools.NumberedChromaticPitchClass(chord)')


def test_NumberedChromaticPitchClass___init____10( ):
   '''Init from named pitch class string.'''

   assert pitchtools.NumberedChromaticPitchClass('c').number == 0
   assert pitchtools.NumberedChromaticPitchClass('cs').number == 1
   assert pitchtools.NumberedChromaticPitchClass('cf').number == 11
   assert pitchtools.NumberedChromaticPitchClass('css').number == 2
