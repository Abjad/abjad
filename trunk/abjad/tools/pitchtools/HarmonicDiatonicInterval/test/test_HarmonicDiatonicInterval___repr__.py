from abjad import *


def test_HarmonicDiatonicInterval___repr___01( ):

   interval = pitchtools.HarmonicDiatonicInterval('perfect', 1)
   repr = interval.__repr__( )
   assert  repr == "HarmonicDiatonicInterval(perfect unison)"

   interval = pitchtools.HarmonicDiatonicInterval('augmented', 1)
   repr = interval.__repr__( )
   assert  repr == "HarmonicDiatonicInterval(augmented unison)"

   interval = pitchtools.HarmonicDiatonicInterval('minor', 2)
   repr = interval.__repr__( )
   assert  repr == "HarmonicDiatonicInterval(minor second)"

   interval = pitchtools.HarmonicDiatonicInterval('major', 2)
   repr = interval.__repr__( )
   assert  repr == "HarmonicDiatonicInterval(major second)"

   interval = pitchtools.HarmonicDiatonicInterval('minor', 3)
   repr = interval.__repr__( )
   assert  repr == "HarmonicDiatonicInterval(minor third)"


def test_HarmonicDiatonicInterval___repr___02( ):

   interval = pitchtools.HarmonicDiatonicInterval('perfect', -1)
   repr = interval.__repr__( )
   assert  repr == "HarmonicDiatonicInterval(perfect unison)"

   interval = pitchtools.HarmonicDiatonicInterval('augmented', -1)
   repr = interval.__repr__( )
   assert  repr == "HarmonicDiatonicInterval(augmented unison)"

   interval = pitchtools.HarmonicDiatonicInterval('minor', -2)
   repr = interval.__repr__( )
   assert  repr == "HarmonicDiatonicInterval(minor second)"

   interval = pitchtools.HarmonicDiatonicInterval('major', -2)
   repr = interval.__repr__( )
   assert  repr == "HarmonicDiatonicInterval(major second)"

   interval = pitchtools.HarmonicDiatonicInterval('minor', -3)
   repr = interval.__repr__( )
   assert  repr == "HarmonicDiatonicInterval(minor third)"
