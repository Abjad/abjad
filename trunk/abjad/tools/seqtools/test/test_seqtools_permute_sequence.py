from abjad import *


def test_seqtools_permute_sequence_01( ):
   '''Permute list.
   '''

   assert seqtools.permute_sequence([11, 12, 13, 14], [1, 0, 3, 2]) == [12, 11, 14, 13]


def test_seqtools_permute_sequence_02( ):
   '''Permute tuple.
   '''

   assert seqtools.permute_sequence((11, 12, 13, 14), [1, 0, 3, 2]) == (12, 11, 14, 13)


def test_seqtools_permute_sequence_03( ):
   '''Permute Abjad container.
   '''

   container = Container("c'8 d'8 e'8")
   assert seqtools.permute_sequence(container, [2, 0, 1]) == Container("e'8 c'8 d'8")


def test_seqtools_permute_sequence_04( ):
   '''Permute string.
   '''

   assert seqtools.permute_sequence('heart', [4, 0, 1, 2, 3]) == 'thear'
