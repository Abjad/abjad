from abjad import *
import py.test


def test_pitch_diatonic_to_chromatic_01( ):
   '''Defaults to white keys on the piano, Ionian.'''

   assert pitchtools.diatonic_to_chromatic(0) == 0
   assert pitchtools.diatonic_to_chromatic(1) == 2
   assert pitchtools.diatonic_to_chromatic(2) == 4
   assert pitchtools.diatonic_to_chromatic(3) == 5
   assert pitchtools.diatonic_to_chromatic(4) == 7
   assert pitchtools.diatonic_to_chromatic(5) == 9
   assert pitchtools.diatonic_to_chromatic(6) == 11
   assert pitchtools.diatonic_to_chromatic(7) == 12
   assert pitchtools.diatonic_to_chromatic(8) == 14

   assert pitchtools.diatonic_to_chromatic(-1) == -1
   assert pitchtools.diatonic_to_chromatic(-2) == -3
   assert pitchtools.diatonic_to_chromatic(-3) == -5
   assert pitchtools.diatonic_to_chromatic(-4) == -7
   assert pitchtools.diatonic_to_chromatic(-5) == -8
   assert pitchtools.diatonic_to_chromatic(-6) == -10
   assert pitchtools.diatonic_to_chromatic(-7) == -12
   assert pitchtools.diatonic_to_chromatic(-8) == -13


def test_pitch_diatonic_to_chromatic_02( ):
   '''Diatonic scale can be tranposed.'''

   assert pitchtools.diatonic_to_chromatic(0, 2) == 2
   assert pitchtools.diatonic_to_chromatic(1, 2) == 4
   assert pitchtools.diatonic_to_chromatic(2, 2) == 6
   assert pitchtools.diatonic_to_chromatic(3, 2) == 7
   assert pitchtools.diatonic_to_chromatic(4, 2) == 9
   assert pitchtools.diatonic_to_chromatic(5, 2) == 11
   assert pitchtools.diatonic_to_chromatic(6, 2) == 13
   assert pitchtools.diatonic_to_chromatic(7, 2) == 14
   assert pitchtools.diatonic_to_chromatic(8, 2) == 16
   assert pitchtools.diatonic_to_chromatic(-1, 2) == 1
   assert pitchtools.diatonic_to_chromatic(-2, 2) == -1

   assert pitchtools.diatonic_to_chromatic(0, -1) == -1
   assert pitchtools.diatonic_to_chromatic(1, -1) == 1
   assert pitchtools.diatonic_to_chromatic(2, -1) == 3
   assert pitchtools.diatonic_to_chromatic(3, -1) == 4
   assert pitchtools.diatonic_to_chromatic(4, -1) == 6
   assert pitchtools.diatonic_to_chromatic(5, -1) == 8
   assert pitchtools.diatonic_to_chromatic(6, -1) == 10
   assert pitchtools.diatonic_to_chromatic(7, -1) == 11
   assert pitchtools.diatonic_to_chromatic(8, -1) == 13
   assert pitchtools.diatonic_to_chromatic(-1, -1) == -2
   assert pitchtools.diatonic_to_chromatic(-2, -1) == -4


def test_pitch_diatonic_to_chromatic_03( ):
   '''Diatonic scale can be rotated.'''

   ## Interval sequence 2,1,2,2,2,1, 2
   assert pitchtools.diatonic_to_chromatic(0, 0, 1) == 0
   assert pitchtools.diatonic_to_chromatic(1, 0, 1) == 2
   assert pitchtools.diatonic_to_chromatic(2, 0, 1) == 3
   assert pitchtools.diatonic_to_chromatic(3, 0, 1) == 5
   assert pitchtools.diatonic_to_chromatic(4, 0, 1) == 7
   assert pitchtools.diatonic_to_chromatic(5, 0, 1) == 9
   assert pitchtools.diatonic_to_chromatic(6, 0, 1) == 10
   assert pitchtools.diatonic_to_chromatic(7, 0, 1) == 12
   assert pitchtools.diatonic_to_chromatic(-1, 0, 1) == -2
   assert pitchtools.diatonic_to_chromatic(-2, 0, 1) == -3

   ## Interval sequence 1,2,2,2,1, 2,2
   assert pitchtools.diatonic_to_chromatic(0, 0, 2) == 0
   assert pitchtools.diatonic_to_chromatic(1, 0, 2) == 1
   assert pitchtools.diatonic_to_chromatic(2, 0, 2) == 3
   assert pitchtools.diatonic_to_chromatic(3, 0, 2) == 5
   assert pitchtools.diatonic_to_chromatic(4, 0, 2) == 7
   assert pitchtools.diatonic_to_chromatic(5, 0, 2) == 8
   assert pitchtools.diatonic_to_chromatic(6, 0, 2) == 10
   assert pitchtools.diatonic_to_chromatic(7, 0, 2) == 12
   assert pitchtools.diatonic_to_chromatic(8, 0, 2) == 13
   assert pitchtools.diatonic_to_chromatic(-1, 0, 2) == -2
   assert pitchtools.diatonic_to_chromatic(-2, 0, 2) == -4


def test_pitch_diatonic_to_chromatic_04( ):
   '''Phase must be positive.'''

   assert py.test.raises(AssertionError, 'pitchtools.diatonic_to_chromatic(0, 1, -3)')
