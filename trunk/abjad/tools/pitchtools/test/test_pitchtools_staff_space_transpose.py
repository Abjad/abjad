from abjad import *
import py.test


def test_pitchtools_staff_space_transpose_01( ):

   pitch = Pitch(0)

   assert pitchtools.staff_space_transpose(pitch, 1, 0) == Pitch('dff', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 0.5) == Pitch('dtqf', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 1) == Pitch('df', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 1.5) == Pitch('dqf', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 2) == Pitch('d', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 2.5) == Pitch('dqs', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 3) == Pitch('ds', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 3.5) == Pitch('dtqs', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 4) == Pitch('dss', 4)

   assert py.test.raises(
      KeyError, 'pitchtools.staff_space_transpose(pitch, 1, 4.5)')


def test_pitchtools_staff_space_transpose_02( ):

   pitch = Pitch(0)

   assert pitchtools.staff_space_transpose(pitch, -1, 0) == Pitch('bs', 3)
   assert pitchtools.staff_space_transpose(pitch, -1, -0.5) == Pitch('bqs', 3)
   assert pitchtools.staff_space_transpose(pitch, -1, -1) == Pitch('b', 3)
   assert pitchtools.staff_space_transpose(pitch, -1, -1.5) == Pitch('bqf', 3)
   assert pitchtools.staff_space_transpose(pitch, -1, -2) == Pitch('bf', 3)
   assert pitchtools.staff_space_transpose(pitch, -1, -2.5) == Pitch('btqf', 3)
   assert pitchtools.staff_space_transpose(pitch, -1, -3) == Pitch('bff', 3)
