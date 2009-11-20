from abjad import *


def test_pitchtools_pc_to_pitch_name_flats_01( ):

   assert pitchtools.pc_to_pitch_name_flats(0) == 'c'
   assert pitchtools.pc_to_pitch_name_flats(0.5) == 'dtqf'
   assert pitchtools.pc_to_pitch_name_flats(1) == 'df'
   assert pitchtools.pc_to_pitch_name_flats(1.5) == 'dqf'
   assert pitchtools.pc_to_pitch_name_flats(2) == 'd'
   assert pitchtools.pc_to_pitch_name_flats(2.5) == 'etqf'
