from abjad import *
import py.test


def test_CommentMark___setattr___01( ):
   '''Slots constrain comment attributes.
   '''

   comment = marktools.Comment('foo')

   assert py.test.raises(AttributeError, "comment.foo = 'bar'")
