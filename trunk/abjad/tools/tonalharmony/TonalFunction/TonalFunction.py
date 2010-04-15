from abjad.tools.tonalharmony.ExtentIndicator import ExtentIndicator
from abjad.tools.tonalharmony.InversionIndicator import InversionIndicator
from abjad.tools.tonalharmony.QualityIndicator import QualityIndicator
from abjad.tools.tonalharmony.ScaleDegree import ScaleDegree


class TonalFunction(object):
   '''.. versionadded:: 1.1.2

   Abjad model of functions in tonal harmony: I, I6, I63, V, V7, V43, V42,
   bII, bII6, etc., also i, i6, i63, v, v7, etc.

   Value object that can not be cahnged after instantiation.
   '''

   ## TODO: add _init_by_format_string later ##
   def __init__(self, scale_degree, quality, extent, inversion):
      scale_degree = ScaleDegree(scale_degree)
      self._scale_degree = scale_degree
      quality = QualityIndicator(quality)
      self._quality = quality
      extent = ExtentIndicator(extent)
      self._extent = extent
      inversion = InversionIndicator(inversion)
      self._inversion = inversion

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.scale_degree == arg.scale_degree:
            if self.quality == arg.quality:
               if self.extent == arg.extent:
                  if self.inversion == arg.inversion:
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
   def _format_string(self):
      result = [ ]
      result.append(self._accidental_name_string)
      result.append(self._roman_numeral_string)
      result.append(self.quality.quality_string.title( ))
      result.append(self.extent.name.title( ))
      result.append('In')
      result.append(self.inversion.title)
      return ''.join(result)

   @property
   def _roman_numeral_string(self):
      roman_numeral_string = self.scale_degree.roman_numeral_string
      if not self.quality.is_uppercase:
         roman_numeral_string = roman_numeral_string.lower( )
      return roman_numeral_string

   ## PUBLIC ATTRIBUTES ##

   @property
   def extent(self):
      return self._extent

   @property
   def inversion(self):
      return self._inversion

   @property
   def quality(self):
      return self._quality

   @property
   def scale_degree(self):
      return self._scale_degree
