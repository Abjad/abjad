from abjad import *


def test_NumericPitchClass___add___01( ):
   '''Ascending melodic chromatic interval added to pitch class.'''

   pc = pitchtools.NumericPitchClass(0)
   MCI = pitchtools.MelodicChromaticInterval

   assert pc + MCI(1) == pitchtools.NumericPitchClass(1)
   assert pc + MCI(2) == pitchtools.NumericPitchClass(2)
   assert pc + MCI(3) == pitchtools.NumericPitchClass(3)
   assert pc + MCI(4) == pitchtools.NumericPitchClass(4)
   assert pc + MCI(5) == pitchtools.NumericPitchClass(5)
   assert pc + MCI(6) == pitchtools.NumericPitchClass(6)
   assert pc + MCI(7) == pitchtools.NumericPitchClass(7)
   assert pc + MCI(8) == pitchtools.NumericPitchClass(8)
   assert pc + MCI(9) == pitchtools.NumericPitchClass(9)
   assert pc + MCI(10) == pitchtools.NumericPitchClass(10)
   assert pc + MCI(11) == pitchtools.NumericPitchClass(11)


def test_NumericPitchClass___add___02( ):
   '''Ascending melodic chromatic interval added to pitch class.'''

   pc = pitchtools.NumericPitchClass(0)
   MCI = pitchtools.MelodicChromaticInterval

   assert pc + MCI(12) == pitchtools.NumericPitchClass(0)
   assert pc + MCI(13) == pitchtools.NumericPitchClass(1)
   assert pc + MCI(14) == pitchtools.NumericPitchClass(2)
   assert pc + MCI(15) == pitchtools.NumericPitchClass(3)
   assert pc + MCI(16) == pitchtools.NumericPitchClass(4)
   assert pc + MCI(17) == pitchtools.NumericPitchClass(5)
   assert pc + MCI(18) == pitchtools.NumericPitchClass(6)
   assert pc + MCI(19) == pitchtools.NumericPitchClass(7)
   assert pc + MCI(20) == pitchtools.NumericPitchClass(8)
   assert pc + MCI(21) == pitchtools.NumericPitchClass(9)
   assert pc + MCI(22) == pitchtools.NumericPitchClass(10)
   assert pc + MCI(23) == pitchtools.NumericPitchClass(11)


def test_NumericPitchClass___add___03( ):
   '''Descending melodic chromatic interval added to pitch class.'''

   pc = pitchtools.NumericPitchClass(0)
   MCI = pitchtools.MelodicChromaticInterval

   assert pc + MCI(-1) == pitchtools.NumericPitchClass(11)
   assert pc + MCI(-2) == pitchtools.NumericPitchClass(10)
   assert pc + MCI(-3) == pitchtools.NumericPitchClass(9)
   assert pc + MCI(-4) == pitchtools.NumericPitchClass(8)
   assert pc + MCI(-5) == pitchtools.NumericPitchClass(7)
   assert pc + MCI(-6) == pitchtools.NumericPitchClass(6)
   assert pc + MCI(-7) == pitchtools.NumericPitchClass(5)
   assert pc + MCI(-8) == pitchtools.NumericPitchClass(4)
   assert pc + MCI(-9) == pitchtools.NumericPitchClass(3)
   assert pc + MCI(-10) == pitchtools.NumericPitchClass(2)
   assert pc + MCI(-11) == pitchtools.NumericPitchClass(1)


def test_NumericPitchClass___add___04( ):
   '''Descending melodic chromatic interval added to pitch class.'''

   pc = pitchtools.NumericPitchClass(0)
   MCI = pitchtools.MelodicChromaticInterval

   assert pc + MCI(-12) == pitchtools.NumericPitchClass(0)
   assert pc + MCI(-13) == pitchtools.NumericPitchClass(11)
   assert pc + MCI(-14) == pitchtools.NumericPitchClass(10)
   assert pc + MCI(-15) == pitchtools.NumericPitchClass(9)
   assert pc + MCI(-16) == pitchtools.NumericPitchClass(8)
   assert pc + MCI(-17) == pitchtools.NumericPitchClass(7)
   assert pc + MCI(-18) == pitchtools.NumericPitchClass(6)
   assert pc + MCI(-19) == pitchtools.NumericPitchClass(5)
   assert pc + MCI(-20) == pitchtools.NumericPitchClass(4)
   assert pc + MCI(-21) == pitchtools.NumericPitchClass(3)
   assert pc + MCI(-22) == pitchtools.NumericPitchClass(2)
   assert pc + MCI(-23) == pitchtools.NumericPitchClass(1)


def test_NumericPitchClass___add___05( ):
   '''Melodic chromatic unison added to pitch class.'''

   pc = pitchtools.NumericPitchClass(0)
   MCI = pitchtools.MelodicChromaticInterval

   assert pc + MCI(0) == pitchtools.NumericPitchClass(0)
