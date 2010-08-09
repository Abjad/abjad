from abjad import *


def test_pitchtools_pc_to_pitch_name_sharps_01( ):

   assert pitchtools.pc_to_pitch_name_sharps(0) == 'c'
   assert pitchtools.pc_to_pitch_name_sharps(0.5) == 'cqs'
   assert pitchtools.pc_to_pitch_name_sharps(1) == 'cs'
   assert pitchtools.pc_to_pitch_name_sharps(1.5) == 'ctqs'
   assert pitchtools.pc_to_pitch_name_sharps(2) == 'd'
   assert pitchtools.pc_to_pitch_name_sharps(2.5) == 'dqs'
