from abjad import *
import py.test


def test_seqtools_truncate_subruns_01( ):
   '''Truncate subruns to length 1.'''

   t = [1, 1, 2, 3, 3, 3, 9, 4, 4, 4]
   result = seqtools.truncate_subruns(t)

   assert result == [1, 2, 3, 9, 4]


def test_seqtools_truncate_subruns_02( ):
   '''Truncate subruns to length 1.'''

   t = [ ]
   result = seqtools.truncate_subruns(t)

   assert result == [ ]


def test_seqtools_truncate_subruns_03( ):
   '''Raise TypeError when l is not a list.'''

   assert py.test.raises(TypeError, 'seqtools.truncate_subruns(1)')
