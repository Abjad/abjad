from abjad import *
import py.test


def test_pitch_pentatonic_to_chromatic_01( ):
   '''Defaults to black keys on the piano.
      Interval sequence 2,3,2,2,3'''

   assert pitchtools.pentatonic_to_chromatic(0) == 1
   assert pitchtools.pentatonic_to_chromatic(1) == 3
   assert pitchtools.pentatonic_to_chromatic(2) == 6
   assert pitchtools.pentatonic_to_chromatic(3) == 8
   assert pitchtools.pentatonic_to_chromatic(4) == 10
   assert pitchtools.pentatonic_to_chromatic(5) == 13
   assert pitchtools.pentatonic_to_chromatic(6) == 15
   assert pitchtools.pentatonic_to_chromatic(-1) == -2
   assert pitchtools.pentatonic_to_chromatic(-2) == -4


def test_pitch_pentatonic_to_chromatic_02( ):
   '''Pentatonic scale can be tranposed.'''

   assert pitchtools.pentatonic_to_chromatic(0, 0) == 0
   assert pitchtools.pentatonic_to_chromatic(1, 0) == 2
   assert pitchtools.pentatonic_to_chromatic(2, 0) == 5
   assert pitchtools.pentatonic_to_chromatic(3, 0) == 7
   assert pitchtools.pentatonic_to_chromatic(4, 0) == 9
   assert pitchtools.pentatonic_to_chromatic(5, 0) == 12
   assert pitchtools.pentatonic_to_chromatic(6, 0) == 14
   assert pitchtools.pentatonic_to_chromatic(-1, 0) == -3
   assert pitchtools.pentatonic_to_chromatic(-2, 0) == -5

   assert pitchtools.pentatonic_to_chromatic(0, -1) == -1
   assert pitchtools.pentatonic_to_chromatic(1, -1) == 1
   assert pitchtools.pentatonic_to_chromatic(2, -1) == 4
   assert pitchtools.pentatonic_to_chromatic(3, -1) == 6
   assert pitchtools.pentatonic_to_chromatic(4, -1) == 8
   assert pitchtools.pentatonic_to_chromatic(5, -1) == 11
   assert pitchtools.pentatonic_to_chromatic(6, -1) == 13
   assert pitchtools.pentatonic_to_chromatic(-1, -1) == -4
   assert pitchtools.pentatonic_to_chromatic(-2, -1) == -6


def test_pitch_pentatonic_to_chromatic_03( ):
   '''Pentatonic scale can be rotated.'''

   ### Interval sequence 3,2,2,3,2
   assert pitchtools.pentatonic_to_chromatic(0, 1, 1) == 1
   assert pitchtools.pentatonic_to_chromatic(1, 1, 1) == 4
   assert pitchtools.pentatonic_to_chromatic(2, 1, 1) == 6
   assert pitchtools.pentatonic_to_chromatic(3, 1, 1) == 8
   assert pitchtools.pentatonic_to_chromatic(4, 1, 1) == 11
   assert pitchtools.pentatonic_to_chromatic(5, 1, 1) == 13
   assert pitchtools.pentatonic_to_chromatic(6, 1, 1) == 16
   assert pitchtools.pentatonic_to_chromatic(-1, 1, 1) == -1
   assert pitchtools.pentatonic_to_chromatic(-2, 1, 1) == -4

   ### Interval sequence 2,2,3,2,3
   assert pitchtools.pentatonic_to_chromatic(0, 2, 2) == 2
   assert pitchtools.pentatonic_to_chromatic(1, 2, 2) == 4
   assert pitchtools.pentatonic_to_chromatic(2, 2, 2) == 6
   assert pitchtools.pentatonic_to_chromatic(3, 2, 2) == 9
   assert pitchtools.pentatonic_to_chromatic(4, 2, 2) == 11
   assert pitchtools.pentatonic_to_chromatic(5, 2, 2) == 14
   assert pitchtools.pentatonic_to_chromatic(6, 2, 2) == 16
   assert pitchtools.pentatonic_to_chromatic(-1, 2, 2) == -1
   assert pitchtools.pentatonic_to_chromatic(-2, 2, 2) == -3


def test_pitch_pentatonic_to_chromatic_04( ):
   '''Phase must be positive.'''

   assert py.test.raises(AssertionError, 'pitchtools.pentatonic_to_chromatic(0, 1, -3)')
