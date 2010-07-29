from abjad import *


def test_metertools_extract_meters_from_measures_in_expr_01( ):
   '''Extract ordered list of meter pairs from components.'''

   t = Staff([RigidMeasure((2, 8), macros.scale(2)),
      RigidMeasure((3, 8), macros.scale(3)),
      RigidMeasure((4, 8), macros.scale(4))])   

   r'''
   \new Staff {
                   \time 2/8
                   c'8
                   d'8
                   \time 3/8
                   c'8
                   d'8
                   e'8
                   \time 4/8
                   c'8
                   d'8
                   e'8
                   f'8
   }
   '''

   meter_list = metertools.extract_meters_from_measures_in_expr(t[:])
   assert meter_list == [(2, 8), (3, 8), (4, 8)]


def test_metertools_extract_meters_from_measures_in_expr_02( ):
   '''Extract ordered list of meter pairs from components.'''

   t = Staff(macros.scale(4))

   r'''
   \new Staff {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   meter_list = metertools.extract_meters_from_measures_in_expr(t[:])
   assert meter_list == [ ]
