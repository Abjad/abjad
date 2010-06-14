from abjad import *
import py.test


def test_iterate_get_measure_number_01( ):

   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
   pitchtools.diatonicize(t)

   assert iterate.get_measure_number(t, 1) is t[0]
   assert iterate.get_measure_number(t, 2) is t[1]
   assert iterate.get_measure_number(t, 3) is t[2]



def test_iterate_get_measure_number_02( ):

   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
   pitchtools.diatonicize(t)

   assert py.test.raises(ValueError, 'iterate.get_measure_number(t, -1)')
