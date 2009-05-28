from abjad import *


def test_listtools_truncate_subruns_01( ):
   '''Truncate subruns to length 1.'''

   t = [1, 1, 2, 3, 3, 3, 9, 4, 4, 4]
   result = listtools.truncate_subruns(t)

   assert result == [1, 2, 3, 9, 4]


def test_listtools_truncate_subruns_02( ):
   '''Truncate subruns to length 1.'''

   t = [ ]
   result = listtools.truncate_subruns(t)

   assert result == [ ]
