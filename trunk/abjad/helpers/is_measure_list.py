from abjad.helpers.contiguity import _are_successive_components
from abjad.measure.base import _Measure


def _is_measure_list(measure_list):
   '''True when

         1. measure_list is a Python list and either

         2. all elements in measure_list are orphan Abjad measures, or
         3. all elements in measure_list are containerized Abjad measures.

      Otherwise False.

      Intended to type-check helper function input.'''

   try:
      assert _are_successive_components(measure_list)
      assert all([isinstance(x, _Measure) for x in measure_list])
   except AssertionError:
      return False

   return True
