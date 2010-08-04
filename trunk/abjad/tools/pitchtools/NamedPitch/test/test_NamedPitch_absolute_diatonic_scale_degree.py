from abjad import *


def test_NamedPitch_absolute_diatonic_scale_degree_01( ):

   assert pitchtools.NamedPitch(0).absolute_diatonic_scale_degree == 29
   assert pitchtools.NamedPitch(1).absolute_diatonic_scale_degree == 29
   assert pitchtools.NamedPitch(2).absolute_diatonic_scale_degree == 30
   assert pitchtools.NamedPitch(3).absolute_diatonic_scale_degree == 31
   assert pitchtools.NamedPitch(4).absolute_diatonic_scale_degree == 31
   assert pitchtools.NamedPitch(5).absolute_diatonic_scale_degree == 32
   assert pitchtools.NamedPitch(6).absolute_diatonic_scale_degree == 32
   assert pitchtools.NamedPitch(7).absolute_diatonic_scale_degree == 33
   assert pitchtools.NamedPitch(8).absolute_diatonic_scale_degree == 34
   assert pitchtools.NamedPitch(9).absolute_diatonic_scale_degree == 34
   assert pitchtools.NamedPitch(10).absolute_diatonic_scale_degree == 35
   assert pitchtools.NamedPitch(11).absolute_diatonic_scale_degree == 35
   assert pitchtools.NamedPitch(12).absolute_diatonic_scale_degree == 36
