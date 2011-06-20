from abjad import *
from abjad.tools import seqtools


def test_seqtools_repeat_sequence_to_weight_at_most_01( ):

   assert seqtools.repeat_sequence_to_weight_at_most([5, -5, -5], 23) == [5, -5, -5, 5]
