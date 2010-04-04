from abjad import *
import py.test


def test_iterate_get_nth_namesake_from_01( ):

   t = Staff(construct.scale(4))
   
   assert iterate.get_nth_namesake_from(t[0], 0) is t[0]
   assert iterate.get_nth_namesake_from(t[0], 1) is t[1]
   assert iterate.get_nth_namesake_from(t[0], 2) is t[2]
   assert iterate.get_nth_namesake_from(t[0], 3) is t[3]

   assert iterate.get_nth_namesake_from(t[3], 0) is t[3]
   assert iterate.get_nth_namesake_from(t[3], -1) is t[2]
   assert iterate.get_nth_namesake_from(t[3], -2) is t[1]
   assert iterate.get_nth_namesake_from(t[3], -3) is t[0]


def test_iterate_get_nth_namesake_from_02( ):

   t = Staff(construct.scale(4))
   
   assert py.test.raises(IndexError, 'iterate.get_nth_namesake_from(t[0], 99)')
