from abjad import *
import py.test


def test_pitchtools_staff_space_transpose_01( ):

   pitch = NamedPitch(0)

   assert pitchtools.staff_space_transpose(pitch, 1, 0) == NamedPitch('dff', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 0.5) == NamedPitch('dtqf', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 1) == NamedPitch('df', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 1.5) == NamedPitch('dqf', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 2) == NamedPitch('d', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 2.5) == NamedPitch('dqs', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 3) == NamedPitch('ds', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 3.5) == NamedPitch('dtqs', 4)
   assert pitchtools.staff_space_transpose(pitch, 1, 4) == NamedPitch('dss', 4)

   assert py.test.raises(
      KeyError, 'pitchtools.staff_space_transpose(pitch, 1, 4.5)')


def test_pitchtools_staff_space_transpose_02( ):

   pitch = NamedPitch(0)

   assert pitchtools.staff_space_transpose(pitch, -1, 0) == NamedPitch('bs', 3)
   assert pitchtools.staff_space_transpose(pitch, -1, -0.5) == NamedPitch('bqs', 3)
   assert pitchtools.staff_space_transpose(pitch, -1, -1) == NamedPitch('b', 3)
   assert pitchtools.staff_space_transpose(pitch, -1, -1.5) == NamedPitch('bqf', 3)
   assert pitchtools.staff_space_transpose(pitch, -1, -2) == NamedPitch('bf', 3)
   assert pitchtools.staff_space_transpose(pitch, -1, -2.5) == NamedPitch('btqf', 3)
   assert pitchtools.staff_space_transpose(pitch, -1, -3) == NamedPitch('bff', 3)
