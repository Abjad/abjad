from abjad.tools import seqtools
from abjad.tools import mathtools
from abjad.tools.pitchtools._PitchSegment import _PitchSegment
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


class NamedChromaticPitchSegment(_PitchSegment):
   '''.. versionadded:: 1.1.2

   The Abjad model of a named chromatic pitch segment::

      abjad> pitchtools.NamedChromaticPitchSegment(['bf', 'bqf', "fs'", "g'", 'bqf', "g'"])
      NamedChromaticPitchSegment(['bf', 'bqf', "fs'", "g'", 'bqf', "g'"])

   Named chromtic pitch segments are immutable.
   '''

   #def __new__(self, pitch_tokens):
   def __new__(self, *args):
      if len(args) == 1 and isinstance(args[0], str):
            pitches = [NamedChromaticPitch(x) for x in args[0].split( )]
      else:
         pitches = [NamedChromaticPitch(x) for x in args[0]]
      return tuple.__new__(self, pitches)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s("%s")' % (self.__class__.__name__, self._repr_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents_string(self):
      return ', '.join([str(x) for x in self])

   @property
   def _repr_string(self):
      return ' '.join([str(x) for x in self])

   ## PUBLIC ATTRIBUTES ##

   @property
   def harmonic_chromatic_interval_class_segment(self):
      return [
         x.interval_class for x in self.harmonic_chromatic_interval_segment]

   @property
   def harmonic_chromatic_interval_segment(self):
      from abjad.tools import pitchtools
      result = list(mathtools.difference_series(self.numbers))
      result = [-x for x in result]
      return pitchtools.HarmonicChromaticIntervalSegment(result)

   @property
   def harmonic_diatonic_interval_class_segment(self):
      return [x.interval_class for x in self.harmonic_diatonic_interval_segment]

   @property
   def harmonic_diatonic_interval_segment(self):
      from abjad.tools import pitchtools
      result = list(mathtools.difference_series(self.pitches))
      result = [-x for x in result]
      return HarmonicDiatonicIntervalSegment(result)

   @property
   def inflection_point_count(self):
      return len(self.local_minima) + len(self.local_maxima)

   @property
   def interval_class_segment(self):
      from abjad.tools import pitchtools
      pitch_classes = self.pitch_class_segment
      interval_classes = mathtools.difference_series(pitch_classes)
      return pitchtools.InversionEquivalentChromaticIntervalClassSegment(interval_classes)

   @property
   def interval_class_set(self):
      from abjad.tools import pitchtools
      pitch_classes = self.pitch_class_segment
      interval_classes = mathtools.difference_series(pitch_classes)
      return pitchtools.InversionEquivalentChromaticIntervalClassSet(interval_classes)
      
   @property
   def interval_class_vector(self):
      from abjad.tools import pitchtools
      pitch_classes = self.pitch_class_segment
      interval_classes = mathtools.difference_series(pitch_classes)
      return pitchtools.InversionEquivalentChromaticIntervalClassVector(interval_classes)
      
   @property
   def local_minima(self):
      result = [ ]
      if 3 <= len(self):
         for i in range(1, len(self) - 1):
            left, middle, right = self[i-1], self[i], self[i+1]
            if middle < left and middle < right:
               result.append(middle)
      return tuple(result)

   @property
   def local_maxima(self):
      result = [ ]
      if 3 <= len(self):
         for i in range(1, len(self) - 1):
            left, middle, right = self[i-1], self[i], self[i+1]
            if left < middle and right < middle:
               result.append(middle)
      return tuple(result)

   @property
   def melodic_chromatic_interval_class_segment(self):
      return [x.interval_class for x in self.melodic_chromatic_interval_segment]

   @property
   def melodic_chromatic_interval_segment(self):
      from abjad.tools import pitchtools
      result = list(mathtools.difference_series(self.numbers))
      return pitchtools.MelodicChromaticIntervalSegment(result)

   @property
   def melodic_diatonic_interval_class_segment(self):
      return [x.interval_class for x in self.melodic_diatonic_interval_segment]

   @property
   def melodic_diatonic_interval_segment(self):
      from abjad.tools import pitchtools
      result = list(mathtools.difference_series(self.pitches))
      result = [-x for x in result]
      return pitchtools.MelodicDiatonicIntervalSegment(result)

   @property
   def numbers(self):
      return [abs(pitch.numbered_chromatic_pitch) for pitch in self]

   @property
   def pitch_class_segment(self):
      from abjad.tools import pitchtools
      return pitchtools.NumberedChromaticPitchClassSegment([pitch.pitch_class for pitch in self])

   @property
   def pitch_class_set(self):
      from abjad.tools import pitchtools
      return pitchtools.NumberedChromaticPitchClassSet([pitch.pitch_class for pitch in self])

   @property
   def pitch_class_vector(self):
      from abjad.tools import pitchtools
      return pitchtools.PitchClassVector([pitch.pitch_class for pitch in self])

   @property
   def pitch_set(self):
      from abjad.tools import pitchtools
      return pitchtools.NamedChromaticPitchSet(self[:])

   @property
   def pitch_vector(self):
      from abjad.tools import pitchtools
      return pitchtools.PitchVector(self.pitches)

   @property
   def pitches(self):
      return self[:]

   ## PUBLIC METHODS ##

   def transpose(self, melodic_interval):
      '''Transpose pitches in pitch segment by melodic interval
      and emit new pitch segment.'''
      pitches = [pitch + melodic_interval for pitch in self]
      return type(self)(pitches)
