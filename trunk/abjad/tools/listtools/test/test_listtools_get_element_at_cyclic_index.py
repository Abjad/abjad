from abjad import *


def test_listtools_get_element_at_cyclic_index_01( ):
   '''Get element at nonnegative cyclic index.
   '''

   iterable = 'string'

   assert listtools.get_element_at_cyclic_index(iterable, 0) == 's'
   assert listtools.get_element_at_cyclic_index(iterable, 1) == 't'
   assert listtools.get_element_at_cyclic_index(iterable, 2) == 'r'
   assert listtools.get_element_at_cyclic_index(iterable, 3) == 'i'
   assert listtools.get_element_at_cyclic_index(iterable, 4) == 'n'
   assert listtools.get_element_at_cyclic_index(iterable, 5) == 'g'
   assert listtools.get_element_at_cyclic_index(iterable, 6) == 's'
   assert listtools.get_element_at_cyclic_index(iterable, 7) == 't'
   assert listtools.get_element_at_cyclic_index(iterable, 8) == 'r'
   assert listtools.get_element_at_cyclic_index(iterable, 9) == 'i'
   

def test_listtools_get_element_at_cyclic_index_02( ):
   '''Get element at negative cyclic index.
   '''

   iterable = 'string'

   assert listtools.get_element_at_cyclic_index(iterable, -1) == 'g'
   assert listtools.get_element_at_cyclic_index(iterable, -2) == 'n'
   assert listtools.get_element_at_cyclic_index(iterable, -3) == 'i'
   assert listtools.get_element_at_cyclic_index(iterable, -4) == 'r'
   assert listtools.get_element_at_cyclic_index(iterable, -5) == 't'
   assert listtools.get_element_at_cyclic_index(iterable, -6) == 's'
   assert listtools.get_element_at_cyclic_index(iterable, -7) == 'g'
   assert listtools.get_element_at_cyclic_index(iterable, -8) == 'n'
   assert listtools.get_element_at_cyclic_index(iterable, -9) == 'i'
