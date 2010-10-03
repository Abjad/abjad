from abjad import *


def test_pitchtools_apply_accidental_to_named_pitch_01( ):

   assert pitchtools.apply_accidental_to_named_pitch(
      pitchtools.NamedPitch('cs', 4), 'sharp') == pitchtools.NamedPitch('css', 4)
   assert pitchtools.apply_accidental_to_named_pitch(
      pitchtools.NamedPitch('cs', 4), 'flat') == pitchtools.NamedPitch('c', 4)
   assert pitchtools.apply_accidental_to_named_pitch(
      pitchtools.NamedPitch('cs', 4), 'natural') == pitchtools.NamedPitch('cs', 4)
   assert pitchtools.apply_accidental_to_named_pitch(
      pitchtools.NamedPitch('cs', 4), 'quarter sharp') == pitchtools.NamedPitch('ctqs', 4)
