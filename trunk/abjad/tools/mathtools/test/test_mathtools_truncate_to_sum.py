from abjad.tools import mathtools
import py.test


def test_mathtools_truncate_to_sum_01( ):
   '''truncate_to_sum can take a list.'''

   t = mathtools.truncate_to_sum([2,2,2], 0) 

   assert t == [0]
   assert isinstance(t, list)


#def test_mathtools_truncate_to_sum_02( ):
#   '''truncate_to_sum can take a tuple.'''
#   t = mathtools.truncate_to_sum((2,2,2), 0) 
#   assert t == (0,)
#   assert isinstance(t, tuple)


def test_mathtools_truncate_to_sum_02( ):
   '''Raise TypeError when l is not a list.'''

   assert py.test.raises(TypeError, "mathtools.truncate_to_sum('foo')")


def test_mathtools_truncate_to_sum_03( ):
   '''truncate_to_sum does work :-).'''

   ls = [2,2,1]

   t = mathtools.truncate_to_sum(ls, 1) 
   assert t == [1]
   t = mathtools.truncate_to_sum(ls, 2) 
   assert t == [2]
   t = mathtools.truncate_to_sum(ls, 3) 
   assert t == [2,1]
   t = mathtools.truncate_to_sum(ls, 4) 
   assert t == [2,2]
   t = mathtools.truncate_to_sum(ls, 5) 
   assert t == [2,2,1]
   t = mathtools.truncate_to_sum(ls, 6) 
   assert t == [2,2,1]


## ERRORS ##

def test_mathtools_truncate_to_sum_10( ):
   '''Raise ValueError on negative total.'''

   assert py.test.raises(ValueError, 
      't = mathtools.truncate_to_sum([2, 2, 2], -1)')
