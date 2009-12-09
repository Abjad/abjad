from abjad import *


def test_HarmonicCounterpointInterval___init___01( ):

   hcpi = pitchtools.HarmonicCounterpointInterval(15)
   
   assert repr(hcpi) == 'HarmonicCounterpointInterval(15)'
   assert str(hcpi) == '15'
   assert hcpi.number == 15
