from abjad import *
import py.test


def test_annotations_interface_01( ):
   '''Leaf annotations interface has before, after, left, right.'''

   t = Note(1, (1, 4))
   t.annotations.before.append('before')
   t.annotations.after.append('after')
   t.annotations.left.append('left')
   t.annotations.right.append('right')

   r'''before
   opening
   cs'4
   closing
   after'''

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

   r'''before1
   before2
   left1 left2 cs'4 right1 right2
   after1
   after2'''

   assert t.format == "before1\nbefore2\nleft1 left2 cs'4 right1 right2\nafter1\nafter2"


def test_annotations_interface_03( ):
   '''before, after, opening, closing format correctly on Container.'''

   t = Container(scale(4))
   t.annotations.before.append('before')
   t.annotations.after.append('after')
   t.annotations.opening.append('opening')
   t.annotations.closing.append('closing')

   r'''before
   {
           opening
           c'8
           d'8
           e'8
           f'8
           closing
   }
   after'''

   assert t.format == "before\n{\n\topening\n\tc'8\n\td'8\n\te'8\n\tf'8\n\tclosing\n}\nafter"


def test_annotations_interface_05( ):
   '''Multiple before, after, opening, closing format correctly on Container.'''

   t = Container(scale(4))
   t.annotations.before.append('before1')
   t.annotations.before.append('before2')
   t.annotations.after.append('after1')
   t.annotations.after.append('after2')
   t.annotations.opening.append('opening1')
   t.annotations.opening.append('opening2')
   t.annotations.closing.append('closing1')
   t.annotations.closing.append('closing2')

   r'''before1
   before2
   {
           opening1
           opening2
           c'8
           d'8
           e'8
           f'8
           closing1
           closing2
   }
   after1
   after2'''

   assert t.format == "before1\nbefore2\n{\n\topening1\n\topening2\n\tc'8\n\td'8\n\te'8\n\tf'8\n\tclosing1\n\tclosing2\n}\nafter1\nafter2"
