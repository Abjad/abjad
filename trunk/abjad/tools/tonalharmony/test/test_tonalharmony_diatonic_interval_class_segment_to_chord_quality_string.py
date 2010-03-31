from abjad import *


def test_tonalharmony_diatonic_interval_class_segment_to_chord_quality_string_01( ):

   dic_seg = pitchtools.DiatonicIntervalClassSegment([
      pitchtools.DiatonicIntervalClass('minor', 3),
      pitchtools.DiatonicIntervalClass('minor', 3),])
   assert tonalharmony.diatonic_interval_class_segment_to_chord_quality_string(
      dic_seg) == 'diminished'

   dic_seg = pitchtools.DiatonicIntervalClassSegment([
      pitchtools.DiatonicIntervalClass('minor', 3),
      pitchtools.DiatonicIntervalClass('major', 3),])
   assert tonalharmony.diatonic_interval_class_segment_to_chord_quality_string(
      dic_seg) == 'minor'

   dic_seg = pitchtools.DiatonicIntervalClassSegment([
      pitchtools.DiatonicIntervalClass('major', 3),
      pitchtools.DiatonicIntervalClass('minor', 3),])
   assert tonalharmony.diatonic_interval_class_segment_to_chord_quality_string(
      dic_seg) == 'major'
