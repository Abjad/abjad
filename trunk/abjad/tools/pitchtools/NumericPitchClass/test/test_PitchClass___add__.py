from abjad import *


def test_PitchClass___add___01( ):
   '''Ascending melodic chromatic interval added to pitch class.'''

   pc = pitchtools.PitchClass(0)
   MCI = pitchtools.MelodicChromaticInterval

   assert pc + MCI(1) == pitchtools.PitchClass(1)
   assert pc + MCI(2) == pitchtools.PitchClass(2)
   assert pc + MCI(3) == pitchtools.PitchClass(3)
   assert pc + MCI(4) == pitchtools.PitchClass(4)
   assert pc + MCI(5) == pitchtools.PitchClass(5)
   assert pc + MCI(6) == pitchtools.PitchClass(6)
   assert pc + MCI(7) == pitchtools.PitchClass(7)
   assert pc + MCI(8) == pitchtools.PitchClass(8)
   assert pc + MCI(9) == pitchtools.PitchClass(9)
   assert pc + MCI(10) == pitchtools.PitchClass(10)
   assert pc + MCI(11) == pitchtools.PitchClass(11)


def test_PitchClass___add___02( ):
   '''Ascending melodic chromatic interval added to pitch class.'''

   pc = pitchtools.PitchClass(0)
   MCI = pitchtools.MelodicChromaticInterval

   assert pc + MCI(12) == pitchtools.PitchClass(0)
   assert pc + MCI(13) == pitchtools.PitchClass(1)
   assert pc + MCI(14) == pitchtools.PitchClass(2)
   assert pc + MCI(15) == pitchtools.PitchClass(3)
   assert pc + MCI(16) == pitchtools.PitchClass(4)
   assert pc + MCI(17) == pitchtools.PitchClass(5)
   assert pc + MCI(18) == pitchtools.PitchClass(6)
   assert pc + MCI(19) == pitchtools.PitchClass(7)
   assert pc + MCI(20) == pitchtools.PitchClass(8)
   assert pc + MCI(21) == pitchtools.PitchClass(9)
   assert pc + MCI(22) == pitchtools.PitchClass(10)
   assert pc + MCI(23) == pitchtools.PitchClass(11)


def test_PitchClass___add___03( ):
   '''Descending melodic chromatic interval added to pitch class.'''

   pc = pitchtools.PitchClass(0)
   MCI = pitchtools.MelodicChromaticInterval

   assert pc + MCI(-1) == pitchtools.PitchClass(11)
   assert pc + MCI(-2) == pitchtools.PitchClass(10)
   assert pc + MCI(-3) == pitchtools.PitchClass(9)
   assert pc + MCI(-4) == pitchtools.PitchClass(8)
   assert pc + MCI(-5) == pitchtools.PitchClass(7)
   assert pc + MCI(-6) == pitchtools.PitchClass(6)
   assert pc + MCI(-7) == pitchtools.PitchClass(5)
   assert pc + MCI(-8) == pitchtools.PitchClass(4)
   assert pc + MCI(-9) == pitchtools.PitchClass(3)
   assert pc + MCI(-10) == pitchtools.PitchClass(2)
   assert pc + MCI(-11) == pitchtools.PitchClass(1)


def test_PitchClass___add___04( ):
   '''Descending melodic chromatic interval added to pitch class.'''

   pc = pitchtools.PitchClass(0)
   MCI = pitchtools.MelodicChromaticInterval

   assert pc + MCI(-12) == pitchtools.PitchClass(0)
   assert pc + MCI(-13) == pitchtools.PitchClass(11)
   assert pc + MCI(-14) == pitchtools.PitchClass(10)
   assert pc + MCI(-15) == pitchtools.PitchClass(9)
   assert pc + MCI(-16) == pitchtools.PitchClass(8)
   assert pc + MCI(-17) == pitchtools.PitchClass(7)
   assert pc + MCI(-18) == pitchtools.PitchClass(6)
   assert pc + MCI(-19) == pitchtools.PitchClass(5)
   assert pc + MCI(-20) == pitchtools.PitchClass(4)
   assert pc + MCI(-21) == pitchtools.PitchClass(3)
   assert pc + MCI(-22) == pitchtools.PitchClass(2)
   assert pc + MCI(-23) == pitchtools.PitchClass(1)


def test_PitchClass___add___05( ):
   '''Melodic chromatic unison added to pitch class.'''

   pc = pitchtools.PitchClass(0)
   MCI = pitchtools.MelodicChromaticInterval

   assert pc + MCI(0) == pitchtools.PitchClass(0)
