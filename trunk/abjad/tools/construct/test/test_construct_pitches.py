from abjad import *


def test_construct_pitches_01( ):

   assert construct.pitches([ ]) == [ ]
   assert construct.pitches([0]) == [Pitch(0)]
   assert construct.pitches([0, 2, 4]) == [Pitch(0), Pitch(2), Pitch(4)]


def test_construct_pitches_02( ):

   assert construct.pitches([('df', 4)]) == [Pitch('df', 4)]
   assert construct.pitches([Pitch('df', 4)]) == [Pitch('df', 4)]
   assert construct.pitches([('df', 4), 0]) == [Pitch('df', 4), Pitch(0)]
