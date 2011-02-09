from abjad import *
from abjad.tools import sievetools


def test_seqtools_repeat_elements_at_indices_cyclically_01( ):
   '''Raw cycle token.'''

   t = list(seqtools.repeat_elements_at_indices_cyclically(
      range(10), (5, [1, 2]), 3))
   assert t == [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]


def test_seqtools_repeat_elements_at_indices_cyclically_02( ):
   '''Cycle token may be a sieve.'''

   sieve = sievetools.cycle_tokens_to_sieve((5, [1, 2]))
   t = list(seqtools.repeat_elements_at_indices_cyclically(range(10), sieve, 3))
   assert t == [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]
