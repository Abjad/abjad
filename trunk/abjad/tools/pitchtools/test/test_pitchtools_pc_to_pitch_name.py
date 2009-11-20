from abjad import *


def test_pitchtools_pc_to_pitch_name_01( ):

   assert pitchtools.pc_to_pitch_name(0) == 'c'   
   assert pitchtools.pc_to_pitch_name(0.5) == 'cqs'   
   assert pitchtools.pc_to_pitch_name(1) == 'cs'   
   assert pitchtools.pc_to_pitch_name(1.5) == 'dqf'   
   assert pitchtools.pc_to_pitch_name(2) == 'd'   
   assert pitchtools.pc_to_pitch_name(2.5) == 'dqs'   
