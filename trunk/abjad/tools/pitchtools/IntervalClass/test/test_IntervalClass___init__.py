from abjad import *


def test_IntervalClass___init___01( ):
   '''Init from zero.'''


def test_IntervalClass___init__02( ):
   '''Init from positive integer.'''

   ic = pitchtools.IntervalClass(1)
   assert ic.number == 1

   ic = pitchtools.IntervalClass(2)
   assert ic.number == 2

   ic = pitchtools.IntervalClass(3)
   assert ic.number == 3

   ic = pitchtools.IntervalClass(4)
   assert ic.number == 4

   ic = pitchtools.IntervalClass(5)
   assert ic.number == 5

   ic = pitchtools.IntervalClass(6)
   assert ic.number == 6


def test_IntervalClass___init__03( ):
   '''Init from positive float.'''

   ic = pitchtools.IntervalClass(0.5)
   assert ic.number == 0.5

   ic = pitchtools.IntervalClass(1.5)
   assert ic.number == 1.5

   ic = pitchtools.IntervalClass(2.5)
   assert ic.number == 2.5

   ic = pitchtools.IntervalClass(3.5)
   assert ic.number == 3.5

   ic = pitchtools.IntervalClass(4.5)
   assert ic.number == 4.5

   ic = pitchtools.IntervalClass(5.5)
   assert ic.number == 5.5
