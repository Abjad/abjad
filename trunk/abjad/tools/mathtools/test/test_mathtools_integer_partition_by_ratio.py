from abjad import *
import py.test


def test_mathtools_integer_partition_by_ratio_01( ):
   '''Partition integer n according to ratio.'''

   t = mathtools.integer_partition_by_ratio(10, [1])
   assert t == [10]

   t = mathtools.integer_partition_by_ratio(10, [1, 1])
   assert t == [5, 5]

   t = mathtools.integer_partition_by_ratio(10, [1, 1, 1])
   assert t == [3, 4, 3]

   t = mathtools.integer_partition_by_ratio(10, [1, 1, 1, 1])
   assert t == [3, 2, 3, 2]

   t = mathtools.integer_partition_by_ratio(10, [1, 1, 1, 1, 1])
   assert t == [2, 2, 2, 2, 2]


def test_mathtools_integer_partition_by_ratio_02( ):
   '''Partition integer n according to ratio.'''
   
   t = mathtools.integer_partition_by_ratio(10, [1, 2])
   assert t == [3, 7]

   t = mathtools.integer_partition_by_ratio(10, [3, 1])
   assert t == [8, 2]

   t = mathtools.integer_partition_by_ratio(10, [3, 2])
   assert t == [6, 4]


def test_mathtools_integer_partition_by_ratio_03( ):
   '''Raise TypeError on noninteger n.
      Raise ValueError on nonpositive n.'''

   assert py.test.raises(TypeError, 
      "mathtools.integer_partition_by_ratio('foo', [1, 1, 1])")
   assert py.test.raises(ValueError, 
      'mathtools.integer_partition_by_ratio(-1, [1, 1, 1])')
