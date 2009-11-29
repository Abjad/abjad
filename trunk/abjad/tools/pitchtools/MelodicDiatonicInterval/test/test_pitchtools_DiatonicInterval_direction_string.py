from abjad import *


def test_pitchtools_DiatonicInterval_direction_string_01( ):

   assert pitchtools.DiatonicInterval('perfect', 1).direction_string is None
   assert pitchtools.DiatonicInterval('minor', 2).direction_string == \
      'ascending'
   assert pitchtools.DiatonicInterval('major', 2).direction_string == \
      'ascending'
   assert pitchtools.DiatonicInterval('minor', 3).direction_string == \
      'ascending'
   assert pitchtools.DiatonicInterval('major', 3).direction_string == \
      'ascending'


def test_pitchtools_DiatonicInterval_direction_string_02( ):

   assert pitchtools.DiatonicInterval('perfect', -1).direction_string is None
   assert pitchtools.DiatonicInterval('minor', -2).direction_string == \
      'descending'
   assert pitchtools.DiatonicInterval('major', -2).direction_string == \
      'descending'
   assert pitchtools.DiatonicInterval('minor', -3).direction_string == \
      'descending'
   assert pitchtools.DiatonicInterval('major', -3).direction_string == \
      'descending'
