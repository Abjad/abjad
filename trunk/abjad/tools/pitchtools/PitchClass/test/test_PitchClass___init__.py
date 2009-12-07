from abjad import *
import py.test


def test_PitchClass___init___01( ):
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


def test_PitchClass___init___02( ):
   '''Pitch class initialization works with other pitch classes.'''

   pc = pitchtools.PitchClass(pitchtools.PitchClass(0))
   assert pc.number == 0

   pc = pitchtools.PitchClass(pitchtools.PitchClass(12))
   assert pc.number == 0


def test_PitchClass___init___03( ):
   '''PitchClass initialization works with pitches.'''

   pc = pitchtools.PitchClass(Pitch(0))
   assert pc.number == 0

   pc = pitchtools.PitchClass(Pitch(12))
   assert pc.number == 0


def test_PitchClass___init___04( ):
   '''Pitch class initialization works with notes.'''

   note = Note(13, (1, 4))
   pc = pitchtools.PitchClass(note)
   assert pc == pitchtools.PitchClass(1)


def test_PitchClass___init___05( ):
   '''Pitch class initialization works with one-note chords.'''

   chord = Chord([13], (1, 4))
   pc = pitchtools.PitchClass(chord)
   assert pc == pitchtools.PitchClass(1)


def test_PitchClass___init___06( ):
   '''PitchClass initialization raises TypeError on non-numbers, 
   non-PitchClasss.'''

   assert py.test.raises(TypeError, "pitchtools.PitchClass('foo')")


def test_PitchClass___init___07( ):
   '''PitchClass initialization raises TypeError on rest.'''

   rest = Rest((1, 4))
   assert py.test.raises(TypeError, 'pitchtools.PitchClass(rest)')


def test_PitchClass___init___08( ):
   '''PitchClass initialization raises MissingPitchError on empty chord.''' 

   chord = Chord([ ], (1, 4))
   assert py.test.raises(MissingPitchError, 'pitchtools.PitchClass(chord)')
