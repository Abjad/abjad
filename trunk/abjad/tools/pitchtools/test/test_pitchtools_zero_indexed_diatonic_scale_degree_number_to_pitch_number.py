from abjad import *
import py.test


def test_pitchtools_zero_indexed_diatonic_scale_degree_number_to_pitch_number_01( ):
   '''Defaults to white keys on the piano, Ionian.'''

   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(0) == 0
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(1) == 2
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(2) == 4
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(3) == 5
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(4) == 7
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(5) == 9
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(6) == 11
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(7) == 12
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(8) == 14

   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-1) == -1
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-2) == -3
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-3) == -5
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-4) == -7
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-5) == -8
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-6) == -10
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-7) == -12
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-8) == -13


def test_pitchtools_zero_indexed_diatonic_scale_degree_number_to_pitch_number_02( ):
   '''Diatonic scale can be transposed.'''

   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(0, 2) == 2
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(1, 2) == 4
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(2, 2) == 6
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(3, 2) == 7
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(4, 2) == 9
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(5, 2) == 11
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(6, 2) == 13
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(7, 2) == 14
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(8, 2) == 16
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-1, 2) == 1
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-2, 2) == -1

   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(0, -1) == -1
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(1, -1) == 1
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(2, -1) == 3
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(3, -1) == 4
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(4, -1) == 6
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(5, -1) == 8
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(6, -1) == 10
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(7, -1) == 11
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(8, -1) == 13
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-1, -1) == -2
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-2, -1) == -4


def test_pitchtools_zero_indexed_diatonic_scale_degree_number_to_pitch_number_03( ):
   '''Diatonic scale can be rotated.'''

   ## Interval sequence 2,1,2,2,2,1, 2
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(0, 0, 1) == 0
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(1, 0, 1) == 2
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(2, 0, 1) == 3
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(3, 0, 1) == 5
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(4, 0, 1) == 7
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(5, 0, 1) == 9
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(6, 0, 1) == 10
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(7, 0, 1) == 12
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-1, 0, 1) == -2
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-2, 0, 1) == -3

   ## Interval sequence 1,2,2,2,1, 2,2
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(0, 0, 2) == 0
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(1, 0, 2) == 1
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(2, 0, 2) == 3
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(3, 0, 2) == 5
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(4, 0, 2) == 7
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(5, 0, 2) == 8
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(6, 0, 2) == 10
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(7, 0, 2) == 12
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(8, 0, 2) == 13
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-1, 0, 2) == -2
   assert pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(-2, 0, 2) == -4


def test_pitchtools_zero_indexed_diatonic_scale_degree_number_to_pitch_number_04( ):
   '''Phase must be positive.'''

   assert py.test.raises(AssertionError, 
      'pitchtools.zero_indexed_diatonic_scale_degree_number_to_pitch_number(0, 1, -3)')
