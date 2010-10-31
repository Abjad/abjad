from abjad import *
import py.test
py.test.skip('remove or replace with more specific function calls.')


'''Twelve keyword combinations:

   1. fill = 'exact', cyclic = False, overhang = False
   2. fill = 'exact', cyclic = False, overhang = True
   3. fill = 'exact', cyclic = True, overhang = False
   4. fill = 'exact', cyclic = True, overhang = True
   5. fill = 'less', cyclic = False, overhang = False
   6. fill = 'less', cyclic = False, overhang = True
   7. fill = 'less', cyclic = True, overhang = False
   8. fill = 'less', cyclic = True, overhang = True
   9. fill = 'greater', cyclic = False, overhang = False
   10. fill = 'greater', cyclic = False, overhang = True
   11. fill = 'greater', cyclic = True, overhang = False
   12. fill = 'greater', cyclic = True, overhang = True'''


def test_seqtools_group_sequence_elements_by_weights_01( ):
   '''Partition the elements of l into sublists such that sublist
   weights correspond to input weights according to the value of fill.'''

   l = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]

   ## 1
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'exact', cyclic = False, overhang = False)
   assert t == [[3], [3, 3, 3]]

   ## 2
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'exact', cyclic = False, overhang = True)
   assert t == [[3], [3, 3, 3], [4, 4, 4, 4, 5, 5]]

   ## 3
   assert py.test.raises(PartitionError,
      "t = seqtools.group_sequence_elements_by_weights(l, [3, 9], "
      "fill = 'exact', cyclic = True, overhang = False)")

   ## 4
   assert py.test.raises(PartitionError,
      " t = seqtools.group_sequence_elements_by_weights(l, [3, 9], "
      "fill = 'exact', cyclic = True, overhang = True)")

   ## 5
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'less', cyclic = False, overhang = False)
   assert t == [[3], [3, 3, 3]]

   ## 6
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'less', cyclic = False, overhang = True)
   assert t == [[3], [3, 3, 3], [4, 4, 4, 4, 5, 5]]
   
   ## 7
   assert py.test.raises(PartitionError,
      "t = seqtools.group_sequence_elements_by_weights(l, [3, 9], "
      "fill = 'less', cyclic = True, overhang = False)")

   ## 8
   assert py.test.raises(PartitionError,
      "t = seqtools.group_sequence_elements_by_weights(l, [3, 9], "
      "fill = 'less', cyclic = True, overhang = True)")

   ## 9
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'greater', cyclic = False, overhang = False)
   assert t == [[3], [3, 3, 3]]

   ## 10
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'greater', cyclic = False, overhang = True)
   assert t == [[3], [3, 3, 3], [4, 4, 4, 4, 5, 5]]

   ## 11
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'greater', cyclic = True, overhang = False)
   assert t == [[3], [3, 3, 3], [4], [4, 4, 4], [5]]

   ## 12
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'greater', cyclic = True, overhang = True)
   assert t == [[3], [3, 3, 3], [4], [4, 4, 4], [5], [5]]


def test_seqtools_group_sequence_elements_by_weights_02( ):
   '''Partition the elements of l into sublists such that sublist
   weights correspond to input weights according to the value of fill.'''

   l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

   ## 1
   t = seqtools.group_sequence_elements_by_weights(l, [10], 
      fill = 'exact', cyclic = False, overhang = False)
   assert t == [[1, 2, 3, 4]]

   ## 2
   t = seqtools.group_sequence_elements_by_weights(l, [10], 
      fill = 'exact', cyclic = False, overhang = True)
   assert t == [[1, 2, 3, 4], [5, 6, 7, 8, 9, 10]]

   ## 3
   assert py.test.raises(PartitionError, 
      "t = seqtools.group_sequence_elements_by_weights(l, [10], "
      "fill = 'exact', cyclic = True, overhang = False)")

   ## 4
   assert py.test.raises(PartitionError, 
      "t = seqtools.group_sequence_elements_by_weights(l, [10], "
      "fill = 'exact', cyclic = True, overhang = True)")

   ## 5
   t = seqtools.group_sequence_elements_by_weights(l, [10], 
      fill = 'less', cyclic = False, overhang = False)
   assert t == [[1, 2, 3, 4]]

   ## 6
   t = seqtools.group_sequence_elements_by_weights(l, [10], 
      fill = 'less', cyclic = False, overhang = True)
   assert t == [[1, 2, 3, 4], [5, 6, 7, 8, 9, 10]]

   ## 7
   t = seqtools.group_sequence_elements_by_weights(l, [10], 
      fill = 'less', cyclic = True, overhang = False)
   assert t == [[1, 2, 3, 4], [5], [6], [7], [8], [9], [10]]

   ## 8
   t = seqtools.group_sequence_elements_by_weights(l, [10], 
      fill = 'less', cyclic = True, overhang = True)
   assert t == [[1, 2, 3, 4], [5], [6], [7], [8], [9], [10]]

   ## 9
   t = seqtools.group_sequence_elements_by_weights(l, [10], 
      fill = 'greater', cyclic = False, overhang = False)
   assert t == [[1, 2, 3, 4]]

   ## 10
   t = seqtools.group_sequence_elements_by_weights(l, [10], 
      fill = 'greater', cyclic = False, overhang = True)
   assert t == [[1, 2, 3, 4], [5, 6, 7, 8, 9, 10]]

   ## 11
   t = seqtools.group_sequence_elements_by_weights(l, [10], 
      fill = 'greater', cyclic = True, overhang = False)
   assert t == [[1, 2, 3, 4], [5, 6], [7, 8], [9, 10]]

   ## 12
   t = seqtools.group_sequence_elements_by_weights(l, [10], 
      fill = 'greater', cyclic = True, overhang = True)
   assert t == [[1, 2, 3, 4], [5, 6], [7, 8], [9, 10]]


def test_seqtools_group_sequence_elements_by_weights_03( ):
   '''Partition the elements of l into sublists such that sublist
   weights correspond to input weights according to the value of fill.'''

   l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

   ## 1
   assert py.test.raises(PartitionError,
      "t = seqtools.group_sequence_elements_by_weights(l, [20], "
      "fill = 'exact', cyclic = False, overhang = False)")

   ## 2
   assert py.test.raises(PartitionError,
      "t = seqtools.group_sequence_elements_by_weights(l, [20], "
      "fill = 'exact', cyclic = False, overhang = True)")

   ## 3
   assert py.test.raises(PartitionError, 
      "t = seqtools.group_sequence_elements_by_weights(l, [20], "
      "fill = 'exact', cyclic = True, overhang = False)")

   ## 4
   assert py.test.raises(PartitionError, 
      "t = seqtools.group_sequence_elements_by_weights(l, [20], "
      "fill = 'exact', cyclic = True, overhang = True)")

   ## 5
   t = seqtools.group_sequence_elements_by_weights(l, [20], 
      fill = 'less', cyclic = False, overhang = False)
   assert t == [[1, 2, 3, 4, 5]]

   ## 6
   t = seqtools.group_sequence_elements_by_weights(l, [20], 
      fill = 'less', cyclic = False, overhang = True)
   assert t == [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]

   ## 7
   t = seqtools.group_sequence_elements_by_weights(l, [20], 
      fill = 'less', cyclic = True, overhang = False)
   assert t == [[1, 2, 3, 4, 5], [6, 7], [8, 9]]

   ## 8
   t = seqtools.group_sequence_elements_by_weights(l, [20], 
      fill = 'less', cyclic = True, overhang = True)
   assert t == [[1, 2, 3, 4, 5], [6, 7], [8, 9], [10]]

   ## 9
   t = seqtools.group_sequence_elements_by_weights(l, [20], 
      fill = 'greater', cyclic = False, overhang = False)
   assert t == [[1, 2, 3, 4, 5, 6]]

   ## 10
   t = seqtools.group_sequence_elements_by_weights(l, [20], 
      fill = 'greater', cyclic = False, overhang = True)
   assert t == [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10]]

   ## 11
   t = seqtools.group_sequence_elements_by_weights(l, [20], 
      fill = 'greater', cyclic = True, overhang = False)
   assert t == [[1, 2, 3, 4, 5, 6], [7, 8, 9]]

   ## 12
   t = seqtools.group_sequence_elements_by_weights(l, [20], 
      fill = 'greater', cyclic = True, overhang = True)
   assert t == [[1, 2, 3, 4, 5, 6], [7, 8, 9], [10]]


def test_seqtools_group_sequence_elements_by_weights_04( ):
   '''Partition the elements of l into sublists such that sublist
   weights correspond to input weights according to the value of fill.'''

   l = [3] * 10

   ## 1
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'exact', cyclic = False, overhang = False)
   assert t == [[3], [3, 3, 3]]

   ## 2
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'exact', cyclic = False, overhang = True)
   assert t == [[3], [3, 3, 3], [3, 3, 3, 3, 3, 3]]

   ## 3
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'exact', cyclic = True, overhang = False)
   assert t == [[3], [3, 3, 3], [3], [3, 3, 3], [3]]

   ## 4
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'exact', cyclic = True, overhang = True)
   assert t == [[3], [3, 3, 3], [3], [3, 3, 3], [3], [3]]

   ## 5
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'less', cyclic = False, overhang = False)
   assert t == [[3], [3, 3, 3]]

   ## 6
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'less', cyclic = False, overhang = True)
   assert t == [[3], [3, 3, 3], [3, 3, 3, 3, 3, 3]]
   

   ## 7
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'less', cyclic = True, overhang = False)
   assert t == [[3], [3, 3, 3], [3], [3, 3, 3], [3]]

   ## 8
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'less', cyclic = True, overhang = True)
   assert t == [[3], [3, 3, 3], [3], [3, 3, 3], [3], [3]]

   ## 9
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'greater', cyclic = False, overhang = False)
   assert t == [[3], [3, 3, 3]]

   ## 10
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'greater', cyclic = False, overhang = True)
   assert t == [[3], [3, 3, 3], [3, 3, 3, 3, 3, 3]]

   ## 11
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'greater', cyclic = True, overhang = False)
   assert t == [[3], [3, 3, 3], [3], [3, 3, 3], [3]]

   ## 12
   t = seqtools.group_sequence_elements_by_weights(l, [3, 9], 
      fill = 'greater', cyclic = True, overhang = True)
   assert t == [[3], [3, 3, 3], [3], [3, 3, 3], [3], [3]]


def test_seqtools_group_sequence_elements_by_weights_05( ):

   l = [3] * 15

   t = seqtools.group_sequence_elements_by_weights(l, [8, 10], 
      fill = 'less', cyclic = False, overhang = False)
   assert t == [[3, 3], [3, 3, 3]]

   t = seqtools.group_sequence_elements_by_weights(l, [8, 10], 
      fill = 'less', cyclic = True, overhang = False)
   assert t == [[3, 3], [3, 3, 3], [3, 3], [3, 3, 3], [3, 3]]
