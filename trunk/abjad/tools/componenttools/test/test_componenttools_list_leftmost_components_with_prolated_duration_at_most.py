from abjad import *


def test_componenttools_list_leftmost_components_with_prolated_duration_at_most_01( ):
   '''Accumulate maximum number of components from list 
   such that prolated duration of components is no greater
   than prolated duration at input.
   '''

   t = Voice(macros.scale(4))
   components, duration = componenttools.list_leftmost_components_with_prolated_duration_at_most(
      t[:], Duration(1, 4))

   assert components == t[:2]
   assert duration == Duration(2, 8)


def test_componenttools_list_leftmost_components_with_prolated_duration_at_most_02( ):

   t = Voice(macros.scale(4))
   components, duration = componenttools.list_leftmost_components_with_prolated_duration_at_most(
      t[:], Duration(99))

   assert components == t[:]
   assert duration == Duration(4, 8) 
   

def test_componenttools_list_leftmost_components_with_prolated_duration_at_most_03( ):

   t = Voice(macros.scale(4))
   components, duration = componenttools.list_leftmost_components_with_prolated_duration_at_most(
      t[:], Duration(0))

   assert components == [ ]
   assert duration == Duration(0)


def test_componenttools_list_leftmost_components_with_prolated_duration_at_most_04( ):

   t = Voice(macros.scale(4))
   components, duration = componenttools.list_leftmost_components_with_prolated_duration_at_most(
      t[:], Duration(3, 16))

   assert components == t[:1]
   assert duration == Duration(1, 8)
