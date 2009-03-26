from abjad.helpers.assert_components import assert_components
from abjad.measure.base import _Measure


def _is_measure_list(measure_list):
   '''True when measure_list is a Python list of Abjad measures, and either

         1. all measures in list are orphans, or
         2. all measures in list have the same parent.

      Otherwise False.

      Intended to type-check helper function input.'''

   try:
      assert_components(measure_list, contiguity = 'strict', share = 'parent')
      assert all([isinstance(x, _Measure) for x in measure_list])
   except AssertionError:
      return False

   return True
