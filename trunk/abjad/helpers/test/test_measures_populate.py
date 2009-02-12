from abjad import *


def test_measures_populate_01( ):
   '''Populate nonbinary measure with note train.'''



def test_measures_populate_02( ):
   '''Populate nonbinary measure with big-endian tie chain.'''

   t = RigidMeasure((5, 18), [ ])
   measures_populate(t, 'big-endian')

   r'''
      \time 5/18
      \scaleDurations #'(8 . 9) {
         c'4 ~
         c'16
      }
   '''

   assert check(t)
   assert t.format == "\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\tc'4 ~\n\t\tc'16\n\t}"


def test_measures_populate_03( ):
   '''Populate nonbinary measure with little-endian tie chain.'''

   t = RigidMeasure((5, 18), [ ])
   measures_populate(t, 'little-endian')

   r'''
      \time 5/18
      \scaleDurations #'(8 . 9) {
         c'16 ~
         c'4
      }
   '''

   assert check(t)
   assert t.format == "\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\tc'16 ~\n\t\tc'4\n\t}"


def test_measures_populate_04( ):
   '''Populate nonbinary measure with time-scaled skip.'''

   t = RigidMeasure((5, 18), [ ])
   measures_populate(t, 'skip')

   r'''
      \time 5/18
      \scaleDurations #'(8 . 9) {
         s1 * 5/16
      }
   '''
   
   assert check(t)
   assert t.format == "\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\ts1 * 5/16\n\t}"


def test_measures_populate_05( ):
   '''Populate nonbinary measure with meter series.'''

   t = RigidMeasure((5, 18), [ ])
   measures_populate(t, 'meter series')

   r'''
      \time 5/18
      \scaleDurations #'(8 . 9) {
         c'16
         c'16
         c'16
         c'16
         c'16
      }
   '''

   assert check(t)
   assert t.format == "\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}"
