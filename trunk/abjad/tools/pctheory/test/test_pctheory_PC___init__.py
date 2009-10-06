from abjad import *
import py.test


def test_pctheory_PC___init__01( ):
   '''PC initialization works with numbers.'''

   pc = pctheory.PC(0)
   assert pc.number == 0

   pc = pctheory.PC(0.5)
   assert pc.number == 0.5

   pc = pctheory.PC(1)
   assert pc.number == 1

   pc = pctheory.PC(1.5)
   assert pc.number == 1.5


def test_pctheory_PC___init__02( ):
   '''PC initialization works with other PCs.'''

   pc = pctheory.PC(pctheory.PC(0))
   assert pc.number == 0


def test_pctheory_PC___init__03( ):
   '''PC initialization raises TypeError on non-numbers, non-PCs.
   PC initialization raises ValueError outside of [0, 12).'''

   assert py.test.raises(TypeError, "pctheory.PC('foo')")
   assert py.test.raises(ValueError, 'pctheory.PC(99)')
