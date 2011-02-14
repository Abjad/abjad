from fractions import Fraction
from abjad.tools.pitchtools._DiatonicInterval import _DiatonicInterval


class InversionEquivalentDiatonicIntervalClass(_DiatonicInterval):
   '''.. versionadded:: 1.1.2

   Abjad model of inversion-equivalent diatonic interval class::

      abjad> pitchtools.InversionEquivalentDiatonicIntervalClass('-m14')
      InversionEquivalentDiatonicIntervalClass('M2')

   Inversion-equivalent diatonic interval-classes are immutable.
   '''

   def __init__(self, *args):
      from abjad.tools.pitchtools.is_melodic_diatonic_interval_abbreviation import \
         melodic_diatonic_interval_abbreviation_regex
      if len(args) == 1 and isinstance(args[0], type(self)):
         self._init_by_self_reference(args[0])
      elif len(args) == 1 and isinstance(args[0], str):
         match = melodic_diatonic_interval_abbreviation_regex.match(args[0])
         if match is None:
            raise ValueError('"%s" does not have the form of a hdi abbreviation.' % args[0])
         direction_string, quality_abbreviation, number_string = match.groups( )
         quality_string = self._quality_abbreviation_to_quality_string[quality_abbreviation]
         number = int(number_string) 
         self._init_by_quality_string_and_number(quality_string, number)
      elif len(args) == 1 and isinstance(args[0], tuple):
         self.__init__(*args[0])
      elif len(args) == 2:
         self._init_by_quality_string_and_number(*args)
      else:
         raise ValueError('can not initialize diatonic interval class.')

   ## PRIVATE METHODS ##

   def _init_by_quality_string_and_number(self, quality_string, number):
      if number == 0:
         raise ValueError('diatonic intervals can not equal zero.')
      elif abs(number) == 1:
         number = 1
      elif abs(number) % 7 == 0:
         number = 7
      elif abs(number) % 7 == 1:
         number = 8
      else:
         number = abs(number) % 7
      if self._is_representative_number(number):
         quality_string = quality_string
         number = number
      else:
         quality_string = self._invert_quality_string(quality_string)
         number = 9 - number
      object.__setattr__(self, '_quality_string', quality_string)
      object.__setattr__(self, '_number', number)

   def _init_by_self_reference(self, reference):
      quality_string = reference.quality_string
      number = reference.number
      self.__init__(quality_string, number)

   def _invert_quality_string(self, quality_string):
      inversions = {'major': 'minor', 'minor': 'major', 'perfect': 'perfect',
         'augmented': 'diminished', 'diminished': 'augmented'}
      return inversions[quality_string]

   def _is_representative_number(self, arg):
      if isinstance(arg, (int, long, float, Fraction)):
         if 1 <= arg <= 4 or arg == 8:
            return True
      return False 
