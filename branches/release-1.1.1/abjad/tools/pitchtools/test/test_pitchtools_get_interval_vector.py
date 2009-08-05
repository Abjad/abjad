from abjad import *


def test_pitchtools_get_interval_vector_01( ):

   chord = Chord([0, 2, 11], (1, 4))
   vector = pitchtools.get_interval_vector(chord.pitches)

   assert vector == {
      0: 0,
      1: 0,
      2: 1,
      3: 0,
      4: 0,
      5: 0,
      6: 0,
      7: 0,
      8: 0,
      9: 1,
     10: 0,
     11: 1}


def test_pitchtools_get_interval_vector_02( ):

   t = Staff(construct.scale(4) + construct.scale(4) + construct.scale(4))
   pitches = pitchtools.get_pitches(t)
   vector = pitchtools.get_interval_vector(pitches)

   assert vector == {
      0: 12,
      1: 9,
      2: 18,
      3: 9,
      4: 9,
      5: 9,
      6: 0,
      7: 0,
      8: 0,
      9: 0,
     10: 0,
     11: 0}
