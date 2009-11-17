from abjad import *


def test_pitchtools_get_interval_class_vector_01( ):

   chord = Chord([0, 2, 11], (1, 4))
   vector = pitchtools.get_interval_class_vector(chord.pitches)

   assert vector == {
      0: 0,
      1: 1,
      2: 1,
      3: 1,
      4: 0,
      5: 0,
      6: 0}


def test_pitchtools_get_interval_class_vector_02( ):

   t = Staff(construct.scale(4) + construct.scale(4) + construct.scale(4))
   pitches = pitchtools.get_pitches(t)
   vector = pitchtools.get_interval_class_vector(pitches)

   assert vector == {
      0: 12,
      1: 9,
      2: 18,
      3: 9,
      4: 9,
      5: 9,
      6: 0}


def test_pitchtools_get_interval_class_vector_03( ):

   chord = Chord([-2, -1.5, 9], (1, 4))
   vector = pitchtools.get_interval_class_vector(chord.pitches)
   
   assert vector == {
      0:   0,
      0.5: 1,
      1:   1,
      1.5: 1,
      2:   0,
      2.5: 0,
      3:   0,
      3.5: 0,
      4:   0,
      4.5: 0,
      5:   0,
      5.5: 0,
      6:   0}
