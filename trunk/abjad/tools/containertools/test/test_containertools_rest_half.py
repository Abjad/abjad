from abjad import *


def test_containertools_rest_half_01( ):
   '''Rest container of length nine.
      Rest left half and make left half bigger.'''

   t = RigidMeasure((9, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(9))
   containertools.rest_half(t, 'left', 'left', rest_direction = 'automatic')
   assert check.wf(t)
   assert str(t) == "|9/8, r8, r2, a'8, b'8, c''8, d''8|"

   t = RigidMeasure((9, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(9))
   containertools.rest_half(t, 'left', 'left', rest_direction = 'big-endian')
   assert check.wf(t)
   assert str(t) == "|9/8, r2, r8, a'8, b'8, c''8, d''8|"

   t = RigidMeasure((9, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(9))
   containertools.rest_half(t, 'left', 'left', rest_direction = 'little-endian')
   assert check.wf(t)
   assert str(t) == "|9/8, r8, r2, a'8, b'8, c''8, d''8|"


def test_containertools_rest_half_02( ):
   '''Rest container of length nine.
      Rest left half but make right half bigger.'''

   t = RigidMeasure((9, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(9))
   containertools.rest_half(t, 'left', 'left', rest_direction = 'automatic')
   assert check.wf(t)
   assert str(t) == "|9/8, r8, r2, a'8, b'8, c''8, d''8|"

   t = RigidMeasure((9, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(9))
   containertools.rest_half(t, 'left', 'left', rest_direction = 'big-endian')
   assert check.wf(t)
   assert str(t) == "|9/8, r2, r8, a'8, b'8, c''8, d''8|"

   t = RigidMeasure((9, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(9))
   containertools.rest_half(t, 'left', 'left', rest_direction = 'little-endian')
   assert check.wf(t)
   assert str(t) == "|9/8, r8, r2, a'8, b'8, c''8, d''8|"

def test_containertools_rest_half_03( ):
   '''Rest container of length nine.
      Rest right half and make right half bigger.'''

   t = RigidMeasure((9, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(9))
   containertools.rest_half(t, 'right', 'right', rest_direction = 'automatic')
   assert check.wf(t)
   assert str(t) == "|9/8, c'8, d'8, e'8, f'8, r2, r8|"

   t = RigidMeasure((9, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(9))
   containertools.rest_half(t, 'right', 'right', rest_direction = 'big-endian')
   assert check.wf(t)
   assert str(t) == "|9/8, c'8, d'8, e'8, f'8, r2, r8|"

   t = RigidMeasure((9, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(9))
   containertools.rest_half(t, 'right', 'right', rest_direction = 'little-endian')
   assert check.wf(t)
   assert str(t) == "|9/8, c'8, d'8, e'8, f'8, r8, r2|"


def test_containertools_rest_half_04( ):
   '''Rest container of length nine.
      Rest right half but make left half bigger.'''

   t = RigidMeasure((9, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(9))
   containertools.rest_half(t, 'right', 'left', rest_direction = 'automatic')
   assert check.wf(t)
   assert str(t) == "|9/8, c'8, d'8, e'8, f'8, g'8, r2|"

   t = RigidMeasure((9, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(9))
   containertools.rest_half(t, 'right', 'left', rest_direction = 'big-endian')
   assert check.wf(t)
   assert str(t) == "|9/8, c'8, d'8, e'8, f'8, g'8, r2|"

   t = RigidMeasure((9, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(9))
   containertools.rest_half(t, 'right', 'left', rest_direction = 'little-endian')
   assert check.wf(t)
   assert str(t) == "|9/8, c'8, d'8, e'8, f'8, g'8, r2|"
