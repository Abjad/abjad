from abjad import *


def test_pitchtools_DiatonicInterval_staff_spaces_01( ):

   assert pitchtools.DiatonicInterval('perfect', 1).staff_spaces == 0
   assert pitchtools.DiatonicInterval('minor', 2).staff_spaces == 1
   assert pitchtools.DiatonicInterval('major', 2).staff_spaces == 1
   assert pitchtools.DiatonicInterval('minor', 3).staff_spaces == 2
   assert pitchtools.DiatonicInterval('major', 3).staff_spaces == 2
   assert pitchtools.DiatonicInterval('perfect', 4).staff_spaces == 3
   assert pitchtools.DiatonicInterval('augmented', 4).staff_spaces == 3
   assert pitchtools.DiatonicInterval('diminished', 5).staff_spaces == 4
   assert pitchtools.DiatonicInterval('perfect', 5).staff_spaces == 4
   assert pitchtools.DiatonicInterval('minor', 6).staff_spaces == 5
   assert pitchtools.DiatonicInterval('major', 6).staff_spaces == 5
   assert pitchtools.DiatonicInterval('minor', 7).staff_spaces == 6
   assert pitchtools.DiatonicInterval('major', 7).staff_spaces == 6
   assert pitchtools.DiatonicInterval('perfect', 8).staff_spaces == 7


def test_pitchtools_DiatonicInterval_staff_spaces_02( ):

   assert pitchtools.DiatonicInterval('perfect', -1).staff_spaces == 0
   assert pitchtools.DiatonicInterval('minor', -2).staff_spaces == -1
   assert pitchtools.DiatonicInterval('major', -2).staff_spaces == -1
   assert pitchtools.DiatonicInterval('minor', -3).staff_spaces == -2
   assert pitchtools.DiatonicInterval('major', -3).staff_spaces == -2
   assert pitchtools.DiatonicInterval('perfect', -4).staff_spaces == -3
   assert pitchtools.DiatonicInterval('augmented', -4).staff_spaces == -3
   assert pitchtools.DiatonicInterval('diminished', -5).staff_spaces == -4
   assert pitchtools.DiatonicInterval('perfect', -5).staff_spaces == -4
   assert pitchtools.DiatonicInterval('minor', -6).staff_spaces == -5
   assert pitchtools.DiatonicInterval('major', -6).staff_spaces == -5
   assert pitchtools.DiatonicInterval('minor', -7).staff_spaces == -6
   assert pitchtools.DiatonicInterval('major', -7).staff_spaces == -6
   assert pitchtools.DiatonicInterval('perfect', -8).staff_spaces == -7
