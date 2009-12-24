from abjad import *


def test_listtools_get_elements_at_indices_01( ):

   l = list('string of text')
   t = list(listtools.get_elements_at_indices(l, (2, 3, 10, 12)))

   assert t == ['r', 'i', 't', 'x']
