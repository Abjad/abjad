from abjad import *
import py.test
py.test.skip( )


def test_pitchtools_DiatonicInterval_quality_string_01( ):

   assert pitchtools.DiatonicInterval('perfect', 1).quality_string == 'perfect'
   assert pitchtools.DiatonicInterval('minor', 2).quality_string == 'minor'
   assert pitchtools.DiatonicInterval('major', 2).quality_string == 'major'
   assert pitchtools.DiatonicInterval('minor', 3).quality_string == 'minor'
   assert pitchtools.DiatonicInterval('major', 3).quality_string == 'major'
   assert pitchtools.DiatonicInterval('perfect', 4).quality_string == 'perfect'
   assert pitchtools.DiatonicInterval('augmented', 4).quality_string == \
      'augmented'
   assert pitchtools.DiatonicInterval('diminished', 5).quality_string == \
      'diminished'
   assert pitchtools.DiatonicInterval('perfect', 5).quality_string == 'perfect'
