from abjad import *


def test_pitchtools_named_chromatic_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary_01( ):

   chord = Chord([0, 2, 11], (1, 4))
   vector = pitchtools.named_chromatic_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary(chord.pitches)

   assert vector == {
      0: 0,
      1: 1,
      2: 1,
      3: 1,
      4: 0,
      5: 0,
      6: 0}


def test_pitchtools_named_chromatic_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary_02( ):

   t = Staff(macros.scale(4) + macros.scale(4) + macros.scale(4))
   pitches = pitchtools.list_named_pitches_in_expr(t)
   vector = pitchtools.named_chromatic_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary(pitches)

   assert vector == {
      0: 12,
      1: 9,
      2: 18,
      3: 9,
      4: 9,
      5: 9,
      6: 0}


def test_pitchtools_named_chromatic_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary_03( ):

   chord = Chord([-2, -1.5, 9], (1, 4))
   vector = pitchtools.named_chromatic_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary(chord.pitches)
   
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
