from abjad import *


def test_listtools_zip_sequences_nontruncating_01( ):
   '''Zip and do not truncate to the length of the shortest list.'''

   t = listtools.zip_sequences_nontruncating([1, 2, 3, 4], [11, 12, 13])
   assert t == [(1, 11), (2, 12), (3, 13), (4,)]


def test_listtools_zip_sequences_nontruncating_02( ):
   '''Zip and do not truncate to the length of the shortest list.'''

   t = listtools.zip_sequences_nontruncating([1, 2, 3], [11, 12, 13, 14])
   assert t == [(1, 11), (2, 12), (3, 13), (14,)]
