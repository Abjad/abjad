from abjad import *


def test_seqtools_count_length_two_runs_01( ):

   assert seqtools.count_length_two_runs([0, 1, 2, 3, 4, 5]) == 0
   assert seqtools.count_length_two_runs([0, 0, 1, 1, 2, 2]) == 3
   assert seqtools.count_length_two_runs([0, 0, 0, 0, 0, 0]) == 5


def test_seqtools_count_length_two_runs_02( ):
   '''Empty list and length-1 list boundary cases.'''

   assert seqtools.count_length_two_runs([ ]) == 0
   assert seqtools.count_length_two_runs([1]) == 0
