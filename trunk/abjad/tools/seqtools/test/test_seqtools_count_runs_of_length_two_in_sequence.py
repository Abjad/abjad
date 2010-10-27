from abjad import *


def test_seqtools_count_runs_of_length_two_in_sequence_01( ):

   assert seqtools.count_runs_of_length_two_in_sequence([0, 1, 2, 3, 4, 5]) == 0
   assert seqtools.count_runs_of_length_two_in_sequence([0, 0, 1, 1, 2, 2]) == 3
   assert seqtools.count_runs_of_length_two_in_sequence([0, 0, 0, 0, 0, 0]) == 5


def test_seqtools_count_runs_of_length_two_in_sequence_02( ):
   '''Empty list and length-1 list boundary cases.'''

   assert seqtools.count_runs_of_length_two_in_sequence([ ]) == 0
   assert seqtools.count_runs_of_length_two_in_sequence([1]) == 0
