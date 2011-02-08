from abjad import *


def test_seqtools_is_repetition_free_sequence_01( ):

   assert seqtools.is_repetition_free_sequence(range(6))


def test_seqtools_is_repetition_free_sequence_02( ):

   assert not seqtools.is_repetition_free_sequence([0, 1, 2, 2, 4, 5])


def test_seqtools_is_repetition_free_sequence_03( ):
   '''True when expr is an empty sequence.'''

   assert seqtools.is_repetition_free_sequence([ ])


def test_seqtools_is_repetition_free_sequence_04( ):
   '''False when expr is not a sequence.'''

   assert not seqtools.is_repetition_free_sequence(17)
