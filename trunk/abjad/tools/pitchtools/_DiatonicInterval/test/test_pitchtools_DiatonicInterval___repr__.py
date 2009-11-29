from abjad import *


def test_pitchtools_DiatonicInterval___repr___01( ):

   interval = pitchtools.DiatonicInterval('perfect', 1)
   repr = interval.__repr__( )
   assert  repr == "DiatonicInterval(perfect unison)"

   interval = pitchtools.DiatonicInterval('augmented', 1)
   repr = interval.__repr__( )
   assert  repr == "DiatonicInterval(ascending augmented unison)"

   interval = pitchtools.DiatonicInterval('minor', 2)
   repr = interval.__repr__( )
   assert  repr == "DiatonicInterval(ascending minor second)"

   interval = pitchtools.DiatonicInterval('major', 2)
   repr = interval.__repr__( )
   assert  repr == "DiatonicInterval(ascending major second)"

   interval = pitchtools.DiatonicInterval('minor', 3)
   repr = interval.__repr__( )
   assert  repr == "DiatonicInterval(ascending minor third)"


def test_pitchtools_DiatonicInterval___repr___02( ):

   interval = pitchtools.DiatonicInterval('perfect', -1)
   repr = interval.__repr__( )
   assert  repr == "DiatonicInterval(perfect unison)"

   interval = pitchtools.DiatonicInterval('augmented', -1)
   repr = interval.__repr__( )
   assert  repr == "DiatonicInterval(descending augmented unison)"

   interval = pitchtools.DiatonicInterval('minor', -2)
   repr = interval.__repr__( )
   assert  repr == "DiatonicInterval(descending minor second)"

   interval = pitchtools.DiatonicInterval('major', -2)
   repr = interval.__repr__( )
   assert  repr == "DiatonicInterval(descending major second)"

   interval = pitchtools.DiatonicInterval('minor', -3)
   repr = interval.__repr__( )
   assert  repr == "DiatonicInterval(descending minor third)"
