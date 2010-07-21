from abjad import *


def test_MelodicChromaticIntervalClass___init____01( ):

   mcic = pitchtools.MelodicChromaticIntervalClass(3)

   assert repr(mcic) == 'MelodicChromaticIntervalClass(+3)'
   assert str(mcic) == '+3'
   assert mcic.number == 3


def test_MelodicChromaticIntervalClass___init____02( ):
   '''Works with numbers less or equal to -12.'''

   mcic = pitchtools.MelodicChromaticIntervalClass(-12)
   assert repr(mcic) == 'MelodicChromaticIntervalClass(-12)'
   assert str(mcic) == '-12'
   assert mcic.number == -12

   mcic = pitchtools.MelodicChromaticIntervalClass(-13)
   assert repr(mcic) == 'MelodicChromaticIntervalClass(-1)'
   assert str(mcic) == '-1'
   assert mcic.number == -1


def test_MelodicChromaticIntervalClass___init____03( ):
   '''Works with numbers greater than 12.'''

   mcic = pitchtools.MelodicChromaticIntervalClass(12)
   assert repr(mcic) == 'MelodicChromaticIntervalClass(+12)'
   assert str(mcic) == '+12'
   assert mcic.number == 12

   mcic = pitchtools.MelodicChromaticIntervalClass(13)
   assert repr(mcic) == 'MelodicChromaticIntervalClass(+1)'
   assert str(mcic) == '+1'
   assert mcic.number == 1


def test_MelodicChromaticIntervalClass___init____04( ):
   '''Works with other interval class instances.'''

   mcic = pitchtools.MelodicChromaticIntervalClass(12)
   new_mcic = pitchtools.MelodicChromaticIntervalClass(mcic)
   assert repr(mcic) == 'MelodicChromaticIntervalClass(+12)'
   assert str(mcic) == '+12'
   assert mcic.number == 12
