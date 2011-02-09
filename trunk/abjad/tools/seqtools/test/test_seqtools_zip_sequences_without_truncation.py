from abjad import *


def test_seqtools_zip_sequences_without_truncation_01( ):
   '''Zip and do not truncate to the length of the shortest list.'''

   t = seqtools.zip_sequences_without_truncation([1, 2, 3, 4], [11, 12, 13])
   assert t == [(1, 11), (2, 12), (3, 13), (4,)]


def test_seqtools_zip_sequences_without_truncation_02( ):
   '''Zip and do not truncate to the length of the shortest list.'''

   t = seqtools.zip_sequences_without_truncation([1, 2, 3], [11, 12, 13, 14])
   assert t == [(1, 11), (2, 12), (3, 13), (14,)]
