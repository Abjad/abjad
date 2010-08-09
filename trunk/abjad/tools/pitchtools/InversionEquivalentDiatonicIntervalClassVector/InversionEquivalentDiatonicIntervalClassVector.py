from abjad.tools.pitchtools.list_harmonic_diatonic_intervals_in_expr import list_harmonic_diatonic_intervals_in_expr
from abjad.tools.pitchtools.inventory_inversion_equivalent_diatonic_interval_classes import inventory_inversion_equivalent_diatonic_interval_classes


class InversionEquivalentDiatonicIntervalClassVector(dict):
   '''.. versionadded:: 1.1.2

   Diatonic interval class vector::

      abjad> staff = Staff(macros.scale(5))
      abjad> pitchtools.InversionEquivalentDiatonicIntervalClassVector(staff) 
      InversionEquivalentDiatonicIntervalClassVector(P1: 0, aug1: 0, m2: 1, M2: 3, aug2: 0, dim3: 0, m3: 2, M3: 1, dim4: 0, P4: 3, aug4: 0)

   Vector is not quatertone-aware.
   '''

   def __init__(self, expr): 
      self.all_dics = inventory_inversion_equivalent_diatonic_interval_classes( )
      for dic in self.all_dics:
         self[dic] = 0
      for hdi in list_harmonic_diatonic_intervals_in_expr(expr):
         dic = hdi.diatonic_interval_class
         self[dic] += 1

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self._contents_string == arg._contents_string:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._contents_string)

   def __str__(self):
      return '{%s}' % self._contents_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents_string(self):
      parts = [ ]
      for dic in self.all_dics:
         count = self[dic]
         part = '%s: %s' % (dic, count)
         parts.append(part)
      contents_string = ', '.join(parts)
      return contents_string
