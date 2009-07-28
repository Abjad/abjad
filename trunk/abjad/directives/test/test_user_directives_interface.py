from abjad import *
import py.test


def test_user_directives_interface_01( ):
   #'''Leaf directives interface has before, after, left, right.'''
   '''Leaf directives interface has before, after, right.'''

   t = Note(1, (1, 4))
   t.directives.before.append('before')
   t.directives.after.append('after')
   #t.directives.left.append('left')
   t.directives.right.append('right')

   r'''
   before
   opening
   cs'4
   closing
   after'''

   assert t.format == "before\ncs'4 right\nafter"


def test_user_directives_interface_02( ):
   #'''Multiple left, right, before, afters format correctly.'''
   '''Multiple right, before, afters format correctly.'''

   t = Note(1, (1, 4))
   t.directives.before.append('before1')
   t.directives.before.append('before2')
   t.directives.after.append('after1')
   t.directives.after.append('after2')
   #t.directives.left.append('left1')
   #t.directives.left.append('left2')
   t.directives.right.append('right1')
   t.directives.right.append('right2')

   r'''
   before1
   before2
   cs'4 right1 right2
   after1
   after2
   '''

   assert t.format == "before1\nbefore2\ncs'4 right1 right2\nafter1\nafter2"


def test_user_directives_interface_03( ):
   '''before, after, opening, closing format correctly on Container.'''

   t = Container(construct.scale(4))
   t.directives.before.append('before')
   t.directives.after.append('after')
   t.directives.opening.append('opening')
   t.directives.closing.append('closing')

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


def test_user_directives_interface_05( ):
   '''Multiple before, after, opening, closing format correctly on Container.'''

   t = Container(construct.scale(4))
   t.directives.before.append('before1')
   t.directives.before.append('before2')
   t.directives.after.append('after1')
   t.directives.after.append('after2')
   t.directives.opening.append('opening1')
   t.directives.opening.append('opening2')
   t.directives.closing.append('closing1')
   t.directives.closing.append('closing2')

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
