from abjad.core import _Immutable
from abjad.core import _StrictComparator


class _DiatonicPitchClass(_Immutable, _StrictComparator):
   '''.. versionadded:: 1.1.2

   Base class for named diatonic pitch class and numeric diatonic pitch class.
   '''

   ## PRIVATE ATTRIBUTES ##

   _diatonic_pitch_class_number_to_diatonic_pitch_class_name_string = {
      0: 'c', 1: 'd', 2: 'e', 3: 'f', 4: 'g', 5: 'a', 6: 'b'}

   _diatonic_pitch_class_name_string_to_diatonic_pitch_class_number = {
      'c': 0, 'd': 1, 'e': 2, 'f': 3, 'g': 4, 'a': 5, 'b': 6}
