from abjad import *
import py.test


def test_pctheory_PC___init___01( ):
   '''PC initialization works with numbers.'''

   pc = pctheory.PC(0)
   assert pc.number == 0

   pc = pctheory.PC(0.5)
   assert pc.number == 0.5

   pc = pctheory.PC(1)
   assert pc.number == 1

   pc = pctheory.PC(1.5)
   assert pc.number == 1.5

   pc = pctheory.PC(13)
   assert pc.number == 1

   pc = pctheory.PC(13.5)
   assert pc.number == 1.5


def test_pctheory_PC___init___02( ):
   '''PC initialization works with other PCs.'''

   pc = pctheory.PC(pctheory.PC(0))
   assert pc.number == 0

   pc = pctheory.PC(pctheory.PC(12))
   assert pc.number == 0


def test_pctheory_PC___init___03( ):
   '''PC initialization works with pitches.'''

   pc = pctheory.PC(Pitch(0))
   assert pc.number == 0

   pc = pctheory.PC(Pitch(12))
   assert pc.number == 0


def test_pctheory_PC___init___04( ):
   '''PC initialization raises TypeError on non-numbers, non-PCs.'''

   assert py.test.raises(TypeError, "pctheory.PC('foo')")
