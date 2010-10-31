from abjad import *
import py.test


def test_seqtools_repeat_sequence_elements_n_times_each_01( ):

   l = [1, 1, 2, 3, 5, 5, 6]
   t = seqtools.repeat_sequence_elements_n_times_each(l, 2)

   assert t == [1, 1, 1, 1, 2, 2, 3, 3, 5, 5, 5, 5, 6, 6]


def test_seqtools_repeat_sequence_elements_n_times_each_02( ):

   l = [1, -1, 2, -3, 5, -5, 6]
   t = seqtools.repeat_sequence_elements_n_times_each(l, 2)

   assert t == [1, 1, -1, -1, 2, 2, -3, -3, 5, 5, -5, -5, 6, 6]


def test_seqtools_repeat_sequence_elements_n_times_each_03( ):

   assert py.test.raises(
      TypeError, "seqtools.repeat_sequence_elements_n_times_each('foo')")
