from abjad import *


def test_IntervalClass___init____01( ):
   '''Init from zero.'''


def test_IntervalClass___init____02( ):
   '''Init from positive integer.'''

   ic = pitchtools.InversionEquivalentChromaticIntervalClass(1)
   assert ic.number == 1

   ic = pitchtools.InversionEquivalentChromaticIntervalClass(2)
   assert ic.number == 2

   ic = pitchtools.InversionEquivalentChromaticIntervalClass(3)
   assert ic.number == 3

   ic = pitchtools.InversionEquivalentChromaticIntervalClass(4)
   assert ic.number == 4

   ic = pitchtools.InversionEquivalentChromaticIntervalClass(5)
   assert ic.number == 5

   ic = pitchtools.InversionEquivalentChromaticIntervalClass(6)
   assert ic.number == 6


def test_IntervalClass___init____03( ):
   '''Init from positive float.'''

   ic = pitchtools.InversionEquivalentChromaticIntervalClass(0.5)
   assert ic.number == 0.5

   ic = pitchtools.InversionEquivalentChromaticIntervalClass(1.5)
   assert ic.number == 1.5

   ic = pitchtools.InversionEquivalentChromaticIntervalClass(2.5)
   assert ic.number == 2.5

   ic = pitchtools.InversionEquivalentChromaticIntervalClass(3.5)
   assert ic.number == 3.5

   ic = pitchtools.InversionEquivalentChromaticIntervalClass(4.5)
   assert ic.number == 4.5

   ic = pitchtools.InversionEquivalentChromaticIntervalClass(5.5)
   assert ic.number == 5.5
