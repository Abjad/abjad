from abjad import *


def test_pitchtools_clef_and_staff_position_number_to_pitch_01( ):

   clef = Clef('treble')

   pitch = pitchtools.clef_and_staff_position_number_to_pitch(clef, -1)
   assert pitch == Pitch('a', 4)

   pitch = pitchtools.clef_and_staff_position_number_to_pitch(clef, 0)
   assert pitch == Pitch('b', 4)

   pitch = pitchtools.clef_and_staff_position_number_to_pitch(clef, 1)
   assert pitch == Pitch('c', 5)


def test_pitchtools_clef_and_staff_position_number_to_pitch_02( ):

   clef = Clef('alto')

   pitch = pitchtools.clef_and_staff_position_number_to_pitch(clef, -1)
   assert pitch == Pitch('b', 3)

   pitch = pitchtools.clef_and_staff_position_number_to_pitch(clef, 0)
   assert pitch == Pitch('c', 4)

   pitch = pitchtools.clef_and_staff_position_number_to_pitch(clef, 1)
   assert pitch == Pitch('d', 4)


def test_pitchtools_clef_and_staff_position_number_to_pitch_03( ):

   clef = Clef('bass')

   pitch = pitchtools.clef_and_staff_position_number_to_pitch(clef, -1)
   assert pitch == Pitch('c', 3)

   pitch = pitchtools.clef_and_staff_position_number_to_pitch(clef, 0)
   assert pitch == Pitch('d', 3)

   pitch = pitchtools.clef_and_staff_position_number_to_pitch(clef, 1)
   assert pitch == Pitch('e', 3)
