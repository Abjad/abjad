from abjad import *


def test_IntervalClass___eq___01( ):

   ic1 = pitchtools.IntervalClass(1)
   ic2 = pitchtools.IntervalClass(1)
   ic3 = pitchtools.IntervalClass(2)

   assert ic1 == ic2
   assert ic2 == ic1

   assert not ic2 == ic3
   assert not ic3 == ic2

   assert not ic3 == ic1
   assert not ic1 == ic3
