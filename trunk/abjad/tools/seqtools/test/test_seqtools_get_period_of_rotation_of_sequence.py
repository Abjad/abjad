from abjad import *
import py.test


def test_seqtools_get_period_of_rotation_of_sequence_01( ):
  
   assert seqtools.get_period_of_rotation_of_sequence([1, 1, 1, 1, 1, 1], 1) == 1
   assert seqtools.get_period_of_rotation_of_sequence([1, 2, 1, 2, 1, 2], 1) == 2
   assert seqtools.get_period_of_rotation_of_sequence([1, 2, 1, 1, 2, 1], 1) == 3
   assert seqtools.get_period_of_rotation_of_sequence([1, 2, 1, 1, 1, 1], 1) == 6


def test_seqtools_get_period_of_rotation_of_sequence_02( ):
  
   assert seqtools.get_period_of_rotation_of_sequence([1, 1, 1, 1, 1, 1], 2) == 1
   assert seqtools.get_period_of_rotation_of_sequence([1, 2, 1, 2, 1, 2], 2) == 1
   assert seqtools.get_period_of_rotation_of_sequence([1, 2, 1, 1, 2, 1], 2) == 3
   assert seqtools.get_period_of_rotation_of_sequence([1, 2, 1, 1, 1, 1], 2) == 3


def test_seqtools_get_period_of_rotation_of_sequence_03( ):
  
   assert seqtools.get_period_of_rotation_of_sequence([1, 1, 1, 1, 1, 1], 3) == 1
   assert seqtools.get_period_of_rotation_of_sequence([1, 2, 1, 2, 1, 2], 3) == 2
   assert seqtools.get_period_of_rotation_of_sequence([1, 2, 1, 1, 2, 1], 3) == 1
   assert seqtools.get_period_of_rotation_of_sequence([1, 2, 1, 1, 1, 1], 3) == 2


def test_seqtools_get_period_of_rotation_of_sequence_04( ):
  
   assert seqtools.get_period_of_rotation_of_sequence([1, 1, 1, 1, 1, 1], 10) == 1
   assert seqtools.get_period_of_rotation_of_sequence([1, 2, 1, 2, 1, 2], 10) == 1
   assert seqtools.get_period_of_rotation_of_sequence([1, 2, 1, 1, 2, 1], 10) == 3
   assert seqtools.get_period_of_rotation_of_sequence([1, 2, 1, 1, 1, 1], 10) == 3


def test_seqtools_get_period_of_rotation_of_sequence_05( ):
   '''Empty iterable boundary case.
   '''

   assert py.test.raises(ZeroDivisionError, 'seqtools.get_period_of_rotation_of_sequence([ ], 1)')
