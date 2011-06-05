from abjad import *


def test_Meter_profile_nonbinary_01( ):
   #t = Measure((5, 7), [
   #   Tuplet((4, 7), Note(0, (1, 4)) * 5)])
   t = Measure((5, 7), [
      Tuplet((4, 7), Note(0, (1, 4)) * 5)])
   assert contexttools.get_effective_time_signature(t) == contexttools.TimeSignatureMark(5, 7)
   assert contexttools.get_effective_time_signature(t).numerator == 5
   assert contexttools.get_effective_time_signature(t).denominator == 7
   assert contexttools.get_effective_time_signature(t).duration == Duration(5, 7)


def test_Meter_profile_nonbinary_02( ):
   #t = Measure((6, 7), [
   #   Tuplet((4, 7), Note(0, (1, 4)) * 6)])
   t = Measure((6, 7), [
      Tuplet((4, 7), Note(0, (1, 4)) * 6)])
   assert contexttools.get_effective_time_signature(t) == contexttools.TimeSignatureMark(6, 7)
   assert contexttools.get_effective_time_signature(t).numerator == 6
   assert contexttools.get_effective_time_signature(t).denominator == 7
   assert contexttools.get_effective_time_signature(t).duration == Duration(6, 7)
