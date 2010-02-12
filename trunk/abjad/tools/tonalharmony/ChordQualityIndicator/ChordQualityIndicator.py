from abjad.tools.pitchtools.HarmonicDiatonicInterval import \
   HarmonicDiatonicInterval
from abjad.tools.pitchtools.HarmonicDiatonicIntervalSet import \
   HarmonicDiatonicIntervalSet


class ChordQualityIndicator(HarmonicDiatonicIntervalSet):
   '''.. versionadded:: 1.1.2

   Chord quality indicator.
   '''

   def __init__(self, *args):
      if len(args) == 1 and isinstance(args[0], str):
         self._init_triad(args[0])
      elif len(args) == 1 and args[0] == 7:
         self._init_seventh('dominant')
      elif len(args) == 1 and args[0] == 9:
         self._init_ninth('dominant')
      elif len(args) == 2 and args[1] == 7:
         self._init_seventh(args[0])
      elif len(args) == 2 and args[1] == 9:
         self._init_ninth(args[0])
      else:
         raise ValueError('unknown chord quality indicator arguments.')

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self._title_case_name, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _acceptable_extended_qualities(self):
      return ('major', 'minor', 'fully diminshed', 'half diminished')

   @property
   def _acceptable_triad_qualities(self):
      return ('major', 'minor', 'diminished', 'augmented')
   
   @property
   def _title_case_name(self):
      return '%s%s' % (
         self._quality_string.title( ), self._cardinality_string.title( ))

   ## PRIVATE METHODS ##

   def _init_ninth(self, quality_string):
      if quality_string == 'dominant':
         intervals = [HarmonicDiatonicInterval('major', 3),
            HarmonicDiatonicInterval('perfect', 5),
            HarmonicDiatonicInterval('minor', 7),
            HarmonicDiatonicInterval('major', 9)]
      else:
         raise ValueError('triad quality string %s must be in %s.' % (
            quality_string, acceptable_strings))
      intervals.insert(0, HarmonicDiatonicInterval('perfect', 1))
      self.update(intervals)
      self._quality_string = quality_string
      self._cardinality_string = 'ninth'

   def _init_seventh(self, quality_string):
      if quality_string == 'dominant':
         intervals = [HarmonicDiatonicInterval('major', 3),
            HarmonicDiatonicInterval('perfect', 5),
            HarmonicDiatonicInterval('minor', 7)]
      elif quality_string == 'major':
         intervals = [HarmonicDiatonicInterval('major', 3),
            HarmonicDiatonicInterval('perfect', 5),
            HarmonicDiatonicInterval('major', 7)]
      elif quality_string == 'minor':
         intervals = [HarmonicDiatonicInterval('minor', 3),
            HarmonicDiatonicInterval('perfect', 5),
            HarmonicDiatonicInterval('minor', 7)]
      elif quality_string in ('diminished', 'fully diminished'):
         intervals = [HarmonicDiatonicInterval('minor', 3),
            HarmonicDiatonicInterval('diminished', 5),
            HarmonicDiatonicInterval('diminished', 7)]
      elif quality_string == 'half diminished':
         intervals = [HarmonicDiatonicInterval('minor', 3),
            HarmonicDiatonicInterval('perfect', 5),
            HarmonicDiatonicInterval('diminished', 7)]
      else:
         raise ValueError('triad quality string %s must be in %s.' % (
            quality_string, acceptable_strings))
      intervals.insert(0, HarmonicDiatonicInterval('perfect', 1))
      self.update(intervals)
      self._quality_string = quality_string
      self._cardinality_string = 'seventh'

   def _init_triad(self, quality_string):
      if quality_string == 'major':
         intervals = [HarmonicDiatonicInterval('major', 3),
            HarmonicDiatonicInterval('perfect', 5)]
      elif quality_string == 'minor':
         intervals = [HarmonicDiatonicInterval('minor', 3),
            HarmonicDiatonicInterval('perfect', 5)]
      elif quality_string == 'diminished':
         intervals = [HarmonicDiatonicInterval('minor', 3),
            HarmonicDiatonicInterval('diminished', 5)]
      elif quality_string == 'augmented':
         intervals = [HarmonicDiatonicInterval('major', 3),
            HarmonicDiatonicInterval('augmented', 5)]
      else:
         raise ValueError('triad quality string %s must be in %s.' % (
            quality_string, acceptable_strings))
      intervals.insert(0, HarmonicDiatonicInterval('perfect', 1))
      self.update(intervals)
      self._quality_string = quality_string
      self._cardinality_string = 'triad'
