from abjad import *


def test_listtools_partition_sequence_by_weights_01( ):
   '''Partition list into sublists of specified weights.'''

   l = [20, 20, 20, 20]
   
   t = listtools.partition_sequence_by_weights(l, [15])
   assert t == [[15]]

   t = listtools.partition_sequence_by_weights(l, [15], cyclic = True)
   assert t == [[15], [5, 10], [10, 5], [15], [15]]

   t = listtools.partition_sequence_by_weights(l, [15], overhang = True)
   assert t == [[15], [5, 20, 20, 20]]

   t = listtools.partition_sequence_by_weights(l, [15], cyclic = True, overhang = True)
   assert t == [[15], [5, 10], [10, 5], [15], [15], [5]]


def test_listtools_partition_sequence_by_weights_02( ):
   '''Partition list into sublists of specified weights.'''

   l = [20, 20, 20, 20]

   t = listtools.partition_sequence_by_weights(l, [7, 15])
   assert t == [[7], [13, 2]]

   t = listtools.partition_sequence_by_weights(l, [7, 15], cyclic = True)
   assert t == [[7], [13, 2], [7], [11, 4], [7], [9, 6], [7]]

   t = listtools.partition_sequence_by_weights(l, [7, 15], overhang = True)
   assert t == [[7], [13, 2], [18, 20, 20]]

   t = listtools.partition_sequence_by_weights(
      l, [7, 15], cyclic = True, overhang = True)
   assert t == [[7], [13, 2], [7], [11, 4], [7], [9, 6], [7], [7]]


def test_listtools_partition_sequence_by_weights_03( ):
   '''Partition list into sublists of specified weights.'''

   l = [20, -20, 20, -20]

   t = listtools.partition_sequence_by_weights(l, [7, 15])
   assert t == [[7], [13, -2]]

   t = listtools.partition_sequence_by_weights(l, [7, 15], cyclic = True)
   assert t == [[7], [13, -2], [-7], [-11, 4], [7], [9, -6], [-7]]

   t = listtools.partition_sequence_by_weights(l, [7, 15], overhang = True)
   assert t == [[7], [13, -2], [-18, 20, -20]]

   t = listtools.partition_sequence_by_weights(
      l, [7, 15], cyclic = True, overhang = True)
   assert t == [[7], [13, -2], [-7], [-11, 4], [7], [9, -6], [-7], [-7]]


def test_listtools_partition_sequence_by_weights_04( ):
   '''Partition list into sublists of specified weights.'''

   l = [1, 1, 1]

   t = listtools.partition_sequence_by_weights(l, [Fraction(2, 3)])
   assert t == [[Fraction(2, 3)]]

   t = listtools.partition_sequence_by_weights(l, [Fraction(2, 3)], cyclic = True)   
   assert t == [
      [Fraction(2, 3)], 
      [Fraction(1, 3), Fraction(1, 3)], 
      [Fraction(2, 3)], 
      [Fraction(2, 3)]]
   
   t = listtools.partition_sequence_by_weights(l, [Fraction(2, 3)], overhang = True)
   assert t == [[Fraction(2, 3)], [Fraction(1, 3), 1, 1]]

   t = listtools.partition_sequence_by_weights(
      l, [Fraction(2, 3)], cyclic = True, overhang = True)
   assert t == [
      [Fraction(2, 3)], 
      [Fraction(1, 3), Fraction(1, 3)], 
      [Fraction(2, 3)], 
      [Fraction(2, 3)], 
      [Fraction(1, 3)]]   


def test_listtools_partition_sequence_by_weights_05( ):
   '''Partition list into sublists of specified weights.'''

   l = [1, -1, 1]

   t = listtools.partition_sequence_by_weights(l, [Fraction(2, 3)])
   assert t == [[Fraction(2, 3)]]

   t = listtools.partition_sequence_by_weights(l, [Fraction(2, 3)], cyclic = True)   
   assert t == [
      [Fraction(2, 3)], 
      [Fraction(1, 3), Fraction(-1, 3)], 
      [Fraction(-2, 3)], 
      [Fraction(2, 3)]]
   
   t = listtools.partition_sequence_by_weights(l, [Fraction(2, 3)], overhang = True)
   assert t == [[Fraction(2, 3)], [Fraction(1, 3), -1, 1]]

   t = listtools.partition_sequence_by_weights(
      l, [Fraction(2, 3)], cyclic = True, overhang = True)
   assert t == [
      [Fraction(2, 3)], 
      [Fraction(1, 3), Fraction(-1, 3)], 
      [Fraction(-2, 3)], 
      [Fraction(2, 3)], 
      [Fraction(1, 3)]]   
