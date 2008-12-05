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
   '''Multiple left, right, before, afters format correctly.'''
   t = Note(1, (1, 4))
   t.formatter.before.append('before1')
   t.formatter.before.append('before2')
   t.formatter.after.append('after1')
   t.formatter.after.append('after2')
   t.formatter.left.append('left1')
   t.formatter.left.append('left2')
   t.formatter.right.append('right1')
   t.formatter.right.append('right2')
   assert t.format == "before1\nbefore2\nleft1 left2 cs'4 right1 right2\nafter1\nafter2"

def test_leaf_formatter_03( ):
   '''Note.formatter does not have opening or closing.'''
   t = Note(1, (1, 4))
   assert raises(AttributeError, "t.formatter.opening.append('open')")
   assert raises(AttributeError, "t.formatter.closing.append('closing')")
