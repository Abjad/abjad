from abjad import *


def test_chord_center_01( ):
   '''
   Chord center equals the arithmetic mean of all pitch numbers in chord.
   '''
  
   t = Chord([0, 2, 9, 10], (1, 4))
   assert t.center == 5.25


def test_chord_center_02( ):
   '''
   Chord center of one-note chord equals the pitch of the chord.
   '''

   t = Chord([8], (1, 4))
   assert t.center == 8


def test_chord_center_03( ):
   '''
   Chord center of empty chord returns None.
   '''

   t = Chord([ ], (1, 4))
   assert t.center is None
