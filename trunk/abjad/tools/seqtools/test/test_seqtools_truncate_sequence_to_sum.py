from abjad.tools import seqtools
import py.test


def test_seqtools_truncate_sequence_to_sum_01( ):
   '''truncate_to_sum can take a list.'''

   t = seqtools.truncate_sequence_to_sum([2, 2, 2], 0) 

   #assert t == [0]
   assert t == [ ]
   assert isinstance(t, list)


#def test_seqtools_truncate_sequence_to_sum_02( ):
#   '''truncate_to_sum can take a tuple.'''
#   t = seqtools.truncate_sequence_to_sum((2, 2, 2), 0) 
#   assert t == (0, )
#   assert isinstance(t, tuple)


def test_seqtools_truncate_sequence_to_sum_03( ):
   '''Raise TypeError when l is not a list.'''

   assert py.test.raises(TypeError, "seqtools.truncate_sequence_to_sum('foo')")


def test_seqtools_truncate_sequence_to_sum_04( ):
   '''truncate_to_sum does work :-).'''

   ls = [2, 2, 1]

   t = seqtools.truncate_sequence_to_sum(ls, 1) 
   assert t == [1]
   t = seqtools.truncate_sequence_to_sum(ls, 2) 
   assert t == [2]
   t = seqtools.truncate_sequence_to_sum(ls, 3) 
   assert t == [2, 1]
   t = seqtools.truncate_sequence_to_sum(ls, 4) 
   assert t == [2, 2]
   t = seqtools.truncate_sequence_to_sum(ls, 5) 
   assert t == [2, 2, 1]
   t = seqtools.truncate_sequence_to_sum(ls, 6) 
   assert t == [2, 2, 1]


## ERRORS ##

def test_seqtools_truncate_sequence_to_sum_05( ):
   '''Raise ValueError on negative total.'''

   assert py.test.raises(ValueError, 
      't = seqtools.truncate_sequence_to_sum([2, 2, 2], -1)')
