from abjad import *
import py.test


def test_pitchtools_PitchClass___init___01( ):
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


def test_pitchtools_PitchClass___init___02( ):
   '''Pitch class initialization works with other pitch classes.'''

   pc = pitchtools.PitchClass(pitchtools.PitchClass(0))
   assert pc.number == 0

   pc = pitchtools.PitchClass(pitchtools.PitchClass(12))
   assert pc.number == 0


def test_pitchtools_PitchClass___init___03( ):
   '''PitchClass initialization works with pitches.'''

   pc = pitchtools.PitchClass(Pitch(0))
   assert pc.number == 0

   pc = pitchtools.PitchClass(Pitch(12))
   assert pc.number == 0


def test_pitchtools_PitchClass___init___04( ):
   '''PitchClass initialization raises TypeError on non-numbers, non-PitchClasss.'''

   assert py.test.raises(TypeError, "pitchtools.PitchClass('foo')")
