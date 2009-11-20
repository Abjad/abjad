from abjad import *


def test_pitchtools_diatonic_interval_string_to_diatonic_interval_number_01( ):

   assert pitchtools.diatonic_interval_string_to_diatonic_interval_number(
      'unison') == 1

   assert pitchtools.diatonic_interval_string_to_diatonic_interval_number(
      'second') == 2

   assert pitchtools.diatonic_interval_string_to_diatonic_interval_number(
      'third') == 3

   assert pitchtools.diatonic_interval_string_to_diatonic_interval_number(
      'fourth') == 4

   assert pitchtools.diatonic_interval_string_to_diatonic_interval_number(
      'fifth') == 5
