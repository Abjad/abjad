from abjad.tools import listtools
from abjad.tools.pitchtools.MelodicDiatonicInterval import \
   MelodicDiatonicInterval
from abjad.tools.pitchtools.MelodicDiatonicIntervalSegment import \
   MelodicDiatonicIntervalSegment


class Mode(object):
   '''.. versionadded:: 1.1.2

   Diatonic mode. Can be extended for nondiatonic mode.

   Modes with different ascending and descending forms not yet implemented.
   '''

   def __init__(self, mode_name_string):
      mdi_segment = MelodicDiatonicIntervalSegment([ ])
      m2 = MelodicDiatonicInterval('minor', 2)
      M2 = MelodicDiatonicInterval('major', 2)
      dorian = [M2, m2, M2, M2, M2, m2, M2]
      if mode_name_string == 'dorian':
         mdi_segment.extend(listtools.rotate(dorian, 0))
      elif mode_name_string == 'phrygian':
         mdi_segment.extend(listtools.rotate(dorian, -1))
      elif mode_name_string == 'lydian':
         mdi_segment.extend(listtools.rotate(dorian, -2))
      elif mode_name_string == 'mixolydian':
         mdi_segment.extend(listtools.rotate(dorian, -3))
      elif mode_name_string in ('aeolian', 'minor'):
         mdi_segment.extend(listtools.rotate(dorian, -4))
      elif mode_name_string == 'locrian':
         mdi_segment.extend(listtools.rotate(dorian, -5))
      elif mode_name_string in ('ionian', 'major'):
         mdi_segment.extend(listtools.rotate(dorian, -6))
      else:
         raise ValueError("unknown mode name string '%s'." % mode_name_string)
      self._mode_name_string = mode_name_string
      self._melodic_diatonic_interval_segment = mdi_segment
      self._init_named_pitch_class_segment

   ## OVERLOADS ##

   def __len__(self):
      return len(self.melodic_diatonic_interval_segment)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.mode_name_string)

   ## PUBLIC ATTRIBUTES ##

   @property
   def melodic_diatonic_interval_segment(self):
      return self._melodic_diatonic_interval_segment

   @property
   def mode_name_string(self):
      return self._mode_name_string
