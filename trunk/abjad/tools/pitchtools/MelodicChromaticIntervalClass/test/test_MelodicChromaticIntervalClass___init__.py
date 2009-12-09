from abjad import *


def test_MelodicChromaticIntervalClass___init___01( ):

   mcic = pitchtools.MelodicChromaticIntervalClass(3)

   assert repr(mcic) == 'MelodicChromaticIntervalClass(+3)'
   assert str(mcic) == '+3'
   assert mcic.number == 3
