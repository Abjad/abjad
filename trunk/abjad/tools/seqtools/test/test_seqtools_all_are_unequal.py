from abjad import *


def test_seqtools_all_are_unequal_01( ):
   '''True when the elements in input iterable are unique.'''

   assert seqtools.all_are_unequal([1, 2, 3])


def test_seqtools_all_are_unequal_02( ):
   '''False when the elements in input iterable are not unique.'''

   assert not seqtools.all_are_unequal([1, 1, 1, 2, 3])


def test_seqtools_all_are_unequal_03( ):
   '''False when expr is not a sequence.
   '''

   assert not seqtools.all_are_unequal(17)
