from abjad import *


def test_Pitch_absolute_diatonic_scale_degree_01( ):

   assert Pitch(0).absolute_diatonic_scale_degree == 29
   assert Pitch(1).absolute_diatonic_scale_degree == 29
   assert Pitch(2).absolute_diatonic_scale_degree == 30
   assert Pitch(3).absolute_diatonic_scale_degree == 31
   assert Pitch(4).absolute_diatonic_scale_degree == 31
   assert Pitch(5).absolute_diatonic_scale_degree == 32
   assert Pitch(6).absolute_diatonic_scale_degree == 32
   assert Pitch(7).absolute_diatonic_scale_degree == 33
   assert Pitch(8).absolute_diatonic_scale_degree == 34
   assert Pitch(9).absolute_diatonic_scale_degree == 34
   assert Pitch(10).absolute_diatonic_scale_degree == 35
   assert Pitch(11).absolute_diatonic_scale_degree == 35
   assert Pitch(12).absolute_diatonic_scale_degree == 36
