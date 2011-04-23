from abjad import *
import py.test


def test_seqtools_CyclicList___getslice___01( ):

   cyclic_list = seqtools.CyclicList(range(3))

   assert cyclic_list[:2] == [0, 1]
   assert cyclic_list[:10] == [0, 1, 2, 0, 1, 2, 0, 1, 2, 0]
   assert cyclic_list[2:10] == [2, 0, 1, 2, 0, 1, 2, 0]


def test_seqtools_CyclicList___getslice___02( ):

   cyclic_list = seqtools.CyclicList(range(3))

   assert py.test.raises(MemoryError, 'cyclic_list[:]')
   assert py.test.raises(MemoryError, 'cyclic_list[2:]')
