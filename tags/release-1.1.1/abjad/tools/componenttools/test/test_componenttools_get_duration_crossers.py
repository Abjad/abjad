from abjad import *


def test_componenttools_get_duration_crossing_components_01( ):
   '''Staff and first measure cross offset at 1/8.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)

   r'''\new Staff {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
   }'''

   result = componenttools.get_duration_crossers(t, Rational(1, 8))

   assert result == [t, t[0]]


def test_componenttools_get_duration_crossing_components_02( ):
   '''Staff, first measure and first note cross 1/16.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)

   r'''\new Staff {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
   }'''

   result = componenttools.get_duration_crossers(t, Rational(1, 16))

   assert result == [t, t[0], t[0][0]]


def test_componenttools_get_duration_crossing_components_03( ):
   '''Nothing crosses 0.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)

   r'''\new Staff {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
   }'''

   result = componenttools.get_duration_crossers(t, Rational(0))

   assert result == [ ]


def test_componenttools_get_duration_crossing_components_04( ):
   '''Nothing crosses 100.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)

   r'''\new Staff {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
   }'''

   result = componenttools.get_duration_crossers(t, Rational(100))

   assert result == [ ]
