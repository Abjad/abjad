from abjad import *
from py.test import raises


def test_comments_01( ):
   '''Can not overwrite leaf comments.'''
   t = Note(0, (1, 4))
   assert raises(AttributeError, "t.comments = 'foo'")


def test_comments_02( ):
   '''Can not overwrite container comments.'''
   t = Container(Note(0, (1, 4)) * 4)
   assert raises(AttributeError, "t.comments = 'foo'")
