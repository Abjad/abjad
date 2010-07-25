from abjad.exceptions import TonalHarmonyError
from abjad.tools import pitchtools


def diatonic_interval_class_segment_to_chord_quality_string(dic_seg):
   '''.. versionadded:: 1.1.2

   Convert diatonic interval class segment `dic_seg` to chord
   quality string. ::

      abjad> dic_seg = pitchtools.DiatonicIntervalClassSegment([
      ...   pitchtools.DiatonicIntervalClass('major', 3),
      ...   pitchtools.DiatonicIntervalClass('minor', 3),])
      abjad> tonalitytools.diatonic_interval_class_segment_to_chord_quality_string(dic_seg)
      'major'

   .. todo::
      Implement ``diatonic_interval_class_set_to_chord_quality_string( )``.
   '''

   ## Note: the repeated calls to repr( ) in the implementation of
   ##       this function accommodate the fact that the Abjad
   ##       DiatonicIntervalClassSegment inherits from the built-in
   ##       Python list class, which is mutable and designed to
   ##       to be unhashable, ie, not used as the key to a dictionary.
   ##       Since repr( ) returns a string and since the repr( )
   ##       of different DiatonicIntervalClassSegments are guaranteed
   ##       to be unique based on value, storing reprs as dictionary
   ##       keys works fine.

   dic_seg_to_quality_string = {
      ## triads
      repr(pitchtools.DiatonicIntervalClassSegment([
         pitchtools.DiatonicIntervalClass('minor', 3),
         pitchtools.DiatonicIntervalClass('minor', 3),])): 'diminished',
      repr(pitchtools.DiatonicIntervalClassSegment([
         pitchtools.DiatonicIntervalClass('minor', 3),
         pitchtools.DiatonicIntervalClass('major', 3),])): 'minor',
      repr(pitchtools.DiatonicIntervalClassSegment([
         pitchtools.DiatonicIntervalClass('major', 3),
         pitchtools.DiatonicIntervalClass('minor', 3),])): 'major',
      repr(pitchtools.DiatonicIntervalClassSegment([
         pitchtools.DiatonicIntervalClass('major', 3),
         pitchtools.DiatonicIntervalClass('major', 3),])): 'augmented',
      ## seventh chords
      repr(pitchtools.DiatonicIntervalClassSegment([
         pitchtools.DiatonicIntervalClass('minor', 3),
         pitchtools.DiatonicIntervalClass('minor', 3),
         pitchtools.DiatonicIntervalClass('minor', 3),])): 'diminished',
      repr(pitchtools.DiatonicIntervalClassSegment([
         pitchtools.DiatonicIntervalClass('minor', 3),
         pitchtools.DiatonicIntervalClass('minor', 3),
         pitchtools.DiatonicIntervalClass('major', 3),])): 'half diminished',
      repr(pitchtools.DiatonicIntervalClassSegment([
         pitchtools.DiatonicIntervalClass('minor', 3),
         pitchtools.DiatonicIntervalClass('major', 3),
         pitchtools.DiatonicIntervalClass('minor', 3),])): 'minor',
      repr(pitchtools.DiatonicIntervalClassSegment([
         pitchtools.DiatonicIntervalClass('major', 3),
         pitchtools.DiatonicIntervalClass('minor', 3),
         pitchtools.DiatonicIntervalClass('minor', 3),])): 'dominant',
      repr(pitchtools.DiatonicIntervalClassSegment([
         pitchtools.DiatonicIntervalClass('major', 3),
         pitchtools.DiatonicIntervalClass('minor', 3),
         pitchtools.DiatonicIntervalClass('major', 3),])): 'major',
      ## ninth chords
      repr(pitchtools.DiatonicIntervalClassSegment([
         pitchtools.DiatonicIntervalClass('major', 3),
         pitchtools.DiatonicIntervalClass('minor', 3),
         pitchtools.DiatonicIntervalClass('minor', 3),
         pitchtools.DiatonicIntervalClass('major', 3),])): 'dominant',
      }

   try:
      quality_string = dic_seg_to_quality_string[repr(dic_seg)]
   except KeyError:
      raise TonalHarmonyError('unknown diatonic interval class segment: %s' %
         dic_seg)   

   return quality_string
