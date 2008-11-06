from abjad import *
from py.test import raises

def test_leaf_formatter_01( ):
   '''Note.formatter has left, right, before, after.'''
   t = Note(1, (1, 4))
   t.formatter.before.append('before')
   t.formatter.after.append('after')
   t.formatter.left.append('left')
   t.formatter.right.append('right')
   assert t.format == "before\nleft cs'4 right\nafter"

def test_leaf_formatter_02( ):
   '''Note.formatter does not have opening or closing.'''
   t = Note(1, (1, 4))
   assert raises(AttributeError, "t.formatter.opening.append('open')")
   assert raises(AttributeError, "t.formatter.closing.append('closing')")
