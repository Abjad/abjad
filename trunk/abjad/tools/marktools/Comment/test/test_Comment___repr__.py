from abjad import *
from abjad.tools.marktools import Comment


def test_Comment___repr___01( ):
   '''Repr of unattached comment is evaluable.
   '''

   comment_1 = marktools.Comment('foo')
   comment_2 = eval(repr(comment_1))

   assert isinstance(comment_1, marktools.Comment)
   assert isinstance(comment_2, marktools.Comment)
   assert comment_1 == comment_2
