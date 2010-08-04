from abjad import *


def test_Pitch_absolute_diatonic_scale_degree_01( ):

   assert NamedPitch(0).absolute_diatonic_scale_degree == 29
   assert NamedPitch(1).absolute_diatonic_scale_degree == 29
   assert NamedPitch(2).absolute_diatonic_scale_degree == 30
   assert NamedPitch(3).absolute_diatonic_scale_degree == 31
   assert NamedPitch(4).absolute_diatonic_scale_degree == 31
   assert NamedPitch(5).absolute_diatonic_scale_degree == 32
   assert NamedPitch(6).absolute_diatonic_scale_degree == 32
   assert NamedPitch(7).absolute_diatonic_scale_degree == 33
   assert NamedPitch(8).absolute_diatonic_scale_degree == 34
   assert NamedPitch(9).absolute_diatonic_scale_degree == 34
   assert NamedPitch(10).absolute_diatonic_scale_degree == 35
   assert NamedPitch(11).absolute_diatonic_scale_degree == 35
   assert NamedPitch(12).absolute_diatonic_scale_degree == 36
