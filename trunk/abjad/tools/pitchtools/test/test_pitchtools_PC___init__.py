from abjad import *
import py.test


def test_pitchtools_PC___init___01( ):
   '''PC initialization works with numbers.'''

   pc = pitchtools.PC(0)
   assert pc.number == 0

   pc = pitchtools.PC(0.5)
   assert pc.number == 0.5

   pc = pitchtools.PC(1)
   assert pc.number == 1

   pc = pitchtools.PC(1.5)
   assert pc.number == 1.5

   pc = pitchtools.PC(13)
   assert pc.number == 1

   pc = pitchtools.PC(13.5)
   assert pc.number == 1.5


def test_pitchtools_PC___init___02( ):
   '''PC initialization works with other PCs.'''

   pc = pitchtools.PC(pitchtools.PC(0))
   assert pc.number == 0

   pc = pitchtools.PC(pitchtools.PC(12))
   assert pc.number == 0


def test_pitchtools_PC___init___03( ):
   '''PC initialization works with pitches.'''

   pc = pitchtools.PC(Pitch(0))
   assert pc.number == 0

   pc = pitchtools.PC(Pitch(12))
   assert pc.number == 0


def test_pitchtools_PC___init___04( ):
   '''PC initialization raises TypeError on non-numbers, non-PCs.'''

   assert py.test.raises(TypeError, "pitchtools.PC('foo')")
