from abjad import *
import py.test


def test_pitchtools_transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell_01( ):

   pitch = pitchtools.NamedPitch(0)

   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 0) == pitchtools.NamedPitch('dff', 4)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 0.5) == pitchtools.NamedPitch('dtqf', 4)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 1) == pitchtools.NamedPitch('df', 4)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 1.5) == pitchtools.NamedPitch('dqf', 4)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 2) == pitchtools.NamedPitch('d', 4)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 2.5) == pitchtools.NamedPitch('dqs', 4)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 3) == pitchtools.NamedPitch('ds', 4)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 3.5) == pitchtools.NamedPitch('dtqs', 4)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 4) == pitchtools.NamedPitch('dss', 4)

   assert py.test.raises(
      KeyError, 'pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 4.5)')


def test_pitchtools_transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell_02( ):

   pitch = pitchtools.NamedPitch(0)

   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, 0) == pitchtools.NamedPitch('bs', 3)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, -0.5) == pitchtools.NamedPitch('bqs', 3)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, -1) == pitchtools.NamedPitch('b', 3)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, -1.5) == pitchtools.NamedPitch('bqf', 3)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, -2) == pitchtools.NamedPitch('bf', 3)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, -2.5) == pitchtools.NamedPitch('btqf', 3)
   assert pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, -1, -3) == pitchtools.NamedPitch('bff', 3)
