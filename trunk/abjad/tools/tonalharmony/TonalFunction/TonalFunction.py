from abjad.markup import Markup
from abjad.tools.tonalharmony.ExtentIndicator import ExtentIndicator
from abjad.tools.tonalharmony.InversionIndicator import InversionIndicator
from abjad.tools.tonalharmony.QualityIndicator import QualityIndicator
from abjad.tools.tonalharmony.ScaleDegree import ScaleDegree
from abjad.tools.tonalharmony.SuspensionIndicator import SuspensionIndicator
import re


class TonalFunction(object):
   '''.. versionadded:: 1.1.2

   Abjad model of functions in tonal harmony: I, I6, I63, V, V7, V43, V42,
   bII, bII6, etc., also i, i6, i63, v, v7, etc.

   Value object that can not be cahnged after instantiation.
   '''

   def __init__(self, *args):
      if len(args) == 1 and isinstance(args[0], type(self)):
         self._init_by_reference(args[0])
      elif len(args) == 1 and isinstance(args[0], str):
         self._init_by_symbolic_string(args[0])
      elif len(args) == 4:
         self._init_by_scale_degree_quality_extent_and_inversion(*args)
      elif len(args) == 5:
         self._init_with_suspension(*args)
      else:
         raise ValueError('can not initialize tonal function.')

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.scale_degree == arg.scale_degree:
            if self.quality == arg.quality:
               if self.extent == arg.extent:
                  if self.inversion == arg.inversion:
                     if self.suspension == arg.suspension:
                        return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _accidental_name_string(self):
      accidental = self.scale_degree.accidental
      if accidental.is_adjusted:
         return accidental.name.title( )
      return ''

   @property
   def _figured_bass_string(self):
      if self.extent == ExtentIndicator(5):
         if self.inversion == InversionIndicator(0):
            return ''
         elif self.inversion == InversionIndicator(1):
            return '6'
         elif self.inversion == InversionIndicator(2):
            return '64'
         else:
            raise ValueError
      elif self.extent == ExtentIndicator(7):
         if self.inversion == InversionIndicator(0):
            return '7'
         elif self.inversion == InversionIndicator(1):
            return '65'
         elif self.inversion == InversionIndicator(2):
            return '43'
         elif self.inversion == InversionIndicator(3):
            return '42'
         else:
            raise ValueError
      else:
         raise NotImplementedError

   _figured_bass_string_to_extent = {
      '': 5, '6': 5, '64': 5,
      '7': 7, '65': 7, '43': 7, '42': 7,
   }
         
   _figured_bass_string_to_inversion = {
      '': 0, '6': 1, '64': 2,
      '7': 0, '65': 1, '43': 2, '42': 3,
   }
         
   @property
   def _format_string(self):
      result = [ ]
      result.append(self._accidental_name_string)
      result.append(self._roman_numeral_string)
      result.append(self.quality.quality_string.title( ))
      result.append(self.extent.name.title( ))
      result.append('In')
      result.append(self.inversion.title)
      if not self.suspension.is_empty:
         result.append('With')
         result.append(self.suspension.title_string)
      return ''.join(result)

   @property
   def _quality_symbolic_string(self):
      if self.extent == ExtentIndicator(5):
         if self.quality == QualityIndicator('diminished'):
            return 'o'
         elif self.quality == QualityIndicator('augmented'):
            return '+'
         else:
            return ''
      elif self.extent == ExtentIndicator(7):
         if self.quality == QualityIndicator('dominant'):
            return ''
         elif self.quality == QualityIndicator('major'):
            return 'M'
         #elif self.quality == QualityIndicator('minor'):
         #   return 'm'
         elif self.quality == QualityIndicator('diminished'):
            return 'o'
         elif self.quality == QualityIndicator('half diminished'):
            return '@'
         elif self.quality == QualityIndicator('augmented'):
            return '+'
         else:
            return ''
      else:
         raise NotImplementedError
         
   @property
   def _roman_numeral_string(self):
      roman_numeral_string = self.scale_degree.roman_numeral_string
      if not self.quality.is_uppercase:
         roman_numeral_string = roman_numeral_string.lower( )
      return roman_numeral_string

   #_symbolic_string_regex = re.compile(
   #   r'([#|b]*)([i|I|v|V]+)([M|m|o|@|+]?)(\d*)')

   _symbolic_string_regex = re.compile(
      r'([#|b]*)([i|I|v|V]+)([M|m|o|@|+]?)(\d*)(\s*)([#|b]?\d*-?[#|b]?\d*)')

   ## PRIVATE METHODS ##

   def _init_by_reference(self, tonal_function):
      args = (tonal_function.scale_degree, tonal_function.quality,
         tonal_function.extent, tonal_function.inversion)
      self._init_by_scale_degree_quality_extent_and_inversion(self, *args)

   def _init_by_scale_degree_quality_extent_and_inversion(self, *args):
      scale_degree, quality, extent, inversion = args
      scale_degree = ScaleDegree(scale_degree)
      self._scale_degree = scale_degree
      quality = QualityIndicator(quality)
      self._quality = quality
      extent = ExtentIndicator(extent)
      self._extent = extent
      inversion = InversionIndicator(inversion)
      self._inversion = inversion
      self._suspension = SuspensionIndicator( )

   def _init_by_symbolic_string(self, symbolic_string):
      groups = self._symbolic_string_regex.match(symbolic_string).groups( )
      #print groups
      accidental, roman_numeral, quality, figured_bass, ws, suspension = groups
      scale_degree = ScaleDegree(accidental + roman_numeral)
      self._scale_degree = scale_degree
      extent = self._figured_bass_string_to_extent[figured_bass]
      extent = ExtentIndicator(extent)
      self._extent = extent
      uppercase = roman_numeral == roman_numeral.upper( )
      quality = self._get_quality_name(uppercase, quality, extent.number)
      quality = QualityIndicator(quality)
      self._quality = quality
      inversion = self._figured_bass_string_to_inversion[figured_bass]
      inversion = InversionIndicator(inversion)
      self._inversion = inversion
      suspension = SuspensionIndicator(suspension)
      self._suspension = suspension

   def _init_with_suspension(self, *args):
      self._init_by_scale_degree_quality_extent_and_inversion(*args[:-1])
      suspension = args[-1]
      self._suspension = SuspensionIndicator(suspension)

   def _get_quality_name(self, uppercase, quality_string, extent):
      if quality_string == 'o':
         return 'diminished'
      elif quality_string == '@':
         return 'half diminished'
      elif quality_string == '+':
         return 'augmented'
      elif quality_string == 'M':
         return 'major'
      elif quality_string == 'm':
         return 'minor'
      elif extent == 5:
         if quality_string == '' and uppercase:
            return 'major'
         elif quality_string == '' and not uppercase:
            return 'minor'
         else:
            raise ValueError
      elif extent == 7:
         if quality_string == '' and uppercase:
            return 'dominant'
         elif quality_string == '' and not uppercase:
            return 'minor'
         else:
            raise ValueError
      else:
         raise ValueError
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def bass_scale_degree(self):
      root_scale_degree = self.root_scale_degree.number
      bass_scale_degree = root_scale_degree - 1
      bass_scale_degree += 2 * self.inversion.number
      bass_scale_degree %= 7
      bass_scale_degree += 1
      bass_scale_degree = ScaleDegree(bass_scale_degree)
      return bass_scale_degree

   @property
   def extent(self):
      return self._extent

   @property
   def inversion(self):
      return self._inversion

   @property
   def markup(self):
      symbolic_string = self.symbolic_string
      symbolic_string = symbolic_string.replace('#', r'\sharp ')
      return Markup(symbolic_string)

   @property
   def quality(self):
      return self._quality

   @property
   def root_scale_degree(self):
      return self._scale_degree

   ## TODO: deprecate scale_degree in favor of root_scale_degree ##
   @property
   def scale_degree(self):
      return self._scale_degree

   @property
   def suspension(self):
      return self._suspension

   @property
   def symbolic_string(self):
      result = ''
      result += self.scale_degree.accidental.symbolic_string
      result += self._roman_numeral_string
      result += self._quality_symbolic_string
      result += self._figured_bass_string
      result += self.suspension.figured_bass_string
      return result
