from abjad import *


def test_seqtools_get_elements_at_indices_01( ):

   l = list('string of text')
   t = list(seqtools.get_elements_at_indices(l, (2, 3, 10, 12)))

   assert t == ['r', 'i', 't', 'x']
