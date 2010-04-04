from abjad.tools.pitchtools.HarmonicDiatonicInterval import \
   HarmonicDiatonicInterval
from abjad.tools.pitchtools.HarmonicDiatonicIntervalSegment import \
   HarmonicDiatonicIntervalSegment


class ChordQualityIndicator(HarmonicDiatonicIntervalSegment):
   '''.. versionadded:: 1.1.2

   Chord quality indicator.
   '''

   def __init__(self, quality_string, extent = 'triad', inversion = 'root'):
      if extent in ('triad', 5):
         self._init_triad(quality_string)
      elif extent in ('seventh', 7):
         self._init_seventh(quality_string)
      elif extent in ('ninth', 9):
         self._init_ninth(quality_string)
      else:
         raise ValueError('unknown chord quality indicator arguments.')
      self._invert_quality_indicator(inversion)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self._title_case_name, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _acceptable_ninth_qualities(self):
      return ('dominant', )

   @property
   def _acceptable_seventh_qualities(self):
      return ('dominant', 'major', 'minor', 
         'fully diminshed', 'half diminished')

   @property
   def _acceptable_triad_qualities(self):
      return ('major', 'minor', 'diminished', 'augmented')
   
   @property
   def _chord_position_string(self):
      return self.position.title( ).replace(' ', '')
   
   @property
   def _title_case_name(self):
      return '%s%sIn%s' % (self._quality_string.title( ), 
         self.extent_name.title( ), self._chord_position_string)

   ## PRIVATE METHODS ##

   def _init_ninth(self, quality_string):
      if quality_string == 'dominant':
         intervals = [HarmonicDiatonicInterval('major', 3),
            HarmonicDiatonicInterval('perfect', 5),
            HarmonicDiatonicInterval('minor', 7),
            HarmonicDiatonicInterval('major', 9)]
      else:
         raise ValueError("ninth quality string '%s' must be in %s." % (
            quality_string, self._acceptable_ninth_qualities))
      intervals.insert(0, HarmonicDiatonicInterval('perfect', 1))
      self.extend(intervals)
      self._quality_string = quality_string

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
         raise ValueError("seventh quality string '%s' must be in %s." % (
            quality_string, self._acceptable_seventh_qualities))
      intervals.insert(0, HarmonicDiatonicInterval('perfect', 1))
      self.extend(intervals)
      self._quality_string = quality_string

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
         raise ValueError("triad quality string '%s' must be in %s." % (
            quality_string, self._acceptable_triad_qualities))
      intervals.insert(0, HarmonicDiatonicInterval('perfect', 1))
      self.extend(intervals)
      self._quality_string = quality_string

   def _invert_quality_indicator(self, inversion):
      if isinstance(inversion, int):
         self.rotate(-inversion) 
         self._rotation = -inversion
      elif inversion == 'root':
         self._rotation = 0
      elif inversion == 'first':
         self.rotate(-1)
         self._rotation = -1
      elif inversion == 'second':
         self.rotate(-2)
         self._rotation = -2
      elif inversion == 'third':
         self.rotate(-3)
         self._rotation = -3
      elif inversion == 'fourth':
         self.rotate(-4)
         self._rotation = -4
      else:
         raise ValueError('unknown inversion indicator: %s' % inversion)

   ## PUBLIC ATTRIBUTES ##

   @property
   def cardinality(self):
      return len(self)

   @property
   def extent(self):
      from abjad.tools.tonalharmony.chord_class_cardinality_to_extent import \
         chord_class_cardinality_to_extent
      return chord_class_cardinality_to_extent(self.cardinality)

   @property
   def extent_name(self):
      from abjad.tools.tonalharmony.chord_class_extent_to_extent_name import \
         chord_class_extent_to_extent_name
      return chord_class_extent_to_extent_name(self.extent)
      
   @property
   def inversion(self):
      return abs(self.rotation)

   @property
   def position(self):
      if self.rotation == 0:
         return 'root position'
      elif self.rotation == -1:
         return 'first inversion'
      elif self.rotation == -2:
         return 'second inversion'
      elif self.rotation == -3:
         return 'third inversion'
      elif self.rotation == -4:
         return 'fourth inversion'
      else:
         raise ValueError('unknown chord position.')

   @property
   def quality_string(self):
      return self._quality_string

   @property
   def rotation(self):
      return self._rotation
