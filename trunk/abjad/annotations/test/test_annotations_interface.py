from abjad import *
import py.test


def test_annotations_interface_01( ):
   '''Leaf annotations interface has before, after, left, right.'''
   t = Note(1, (1, 4))
   t.annotations.before.append('before')
   t.annotations.after.append('after')
   t.annotations.left.append('left')
   t.annotations.right.append('right')
   assert t.format == "before\nleft cs'4 right\nafter"


def test_annotations_interface_02( ):
   '''Multiple left, right, before, afters format correctly.'''
   t = Note(1, (1, 4))
   t.annotations.before.append('before1')
   t.annotations.before.append('before2')
   t.annotations.after.append('after1')
   t.annotations.after.append('after2')
   t.annotations.left.append('left1')
   t.annotations.left.append('left2')
   t.annotations.right.append('right1')
   t.annotations.right.append('right2')
   assert t.format == "before1\nbefore2\nleft1 left2 cs'4 right1 right2\nafter1\nafter2"


#def test_annotations_interface_03( ):
#   '''Note.formatter does not have opening or closing.'''
#   t = Note(1, (1, 4))
#   assert py.test.raises(
#      AttributeError, "t.annotations.opening.append('open')")
#   assert py.test.raises(
#      AttributeError, "t.annotations.closing.append('closing')")
