from abjad import *


def test_seqtools_repeat_sequence_n_times_01( ):

   g = seqtools.generate_range(1, 6)
   t = list(seqtools.repeat_sequence_n_times(g, 3))
   assert t == [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]


def test_seqtools_repeat_sequence_n_times_02( ):
   '''Yield nothing n is zero.'''

   g = seqtools.generate_range(1, 6)
   t = list(seqtools.repeat_sequence_n_times(g, 0))
   assert t == [ ]
