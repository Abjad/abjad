from abjad import *


def test_MelodicDiatonicInterval___repr___01( ):

   interval = pitchtools.MelodicDiatonicInterval('perfect', 1)
   repr = interval.__repr__( )
   assert  repr == "MelodicDiatonicInterval(perfect unison)"

   interval = pitchtools.MelodicDiatonicInterval('augmented', 1)
   repr = interval.__repr__( )
   assert  repr == "MelodicDiatonicInterval(ascending augmented unison)"

   interval = pitchtools.MelodicDiatonicInterval('minor', 2)
   repr = interval.__repr__( )
   assert  repr == "MelodicDiatonicInterval(ascending minor second)"

   interval = pitchtools.MelodicDiatonicInterval('major', 2)
   repr = interval.__repr__( )
   assert  repr == "MelodicDiatonicInterval(ascending major second)"

   interval = pitchtools.MelodicDiatonicInterval('minor', 3)
   repr = interval.__repr__( )
   assert  repr == "MelodicDiatonicInterval(ascending minor third)"


def test_MelodicDiatonicInterval___repr___02( ):

   interval = pitchtools.MelodicDiatonicInterval('perfect', -1)
   repr = interval.__repr__( )
   assert  repr == "MelodicDiatonicInterval(perfect unison)"

   interval = pitchtools.MelodicDiatonicInterval('augmented', -1)
   repr = interval.__repr__( )
   assert  repr == "MelodicDiatonicInterval(descending augmented unison)"

   interval = pitchtools.MelodicDiatonicInterval('minor', -2)
   repr = interval.__repr__( )
   assert  repr == "MelodicDiatonicInterval(descending minor second)"

   interval = pitchtools.MelodicDiatonicInterval('major', -2)
   repr = interval.__repr__( )
   assert  repr == "MelodicDiatonicInterval(descending major second)"

   interval = pitchtools.MelodicDiatonicInterval('minor', -3)
   repr = interval.__repr__( )
   assert  repr == "MelodicDiatonicInterval(descending minor third)"
