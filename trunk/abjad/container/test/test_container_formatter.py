from abjad import *
from py.test import raises


def test_container_formatter_01( ):
   '''before, after, opening, closing format correctly on Container.'''

   t = Container(Note(1, (1, 4))*4)
   t.formatter.before.append('before')
   t.formatter.after.append('after')
   t.formatter.opening.append('opening')
   t.formatter.closing.append('closing')

   r'''before
   {
   opening
           cs'4
           cs'4
           cs'4
           cs'4
   closing
   }
   after'''

   assert t.format == "before\n{\nopening\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\nclosing\n}\nafter"


def test_container_formatter_02( ):
   '''before, after, opening, closing format correctly on Parallel.'''

   t = Container(Note(1, (1, 4))*4)
   t.parallel = True
   t.formatter.before.append('before')
   t.formatter.after.append('after')
   t.formatter.opening.append('opening')
   t.formatter.closing.append('closing')

   r'''before
   <<
   opening
           cs'4
           cs'4
           cs'4
           cs'4
   closing
   >>
   after'''

   assert t.format == "before\n<<\nopening\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\nclosing\n>>\nafter"


def test_container_formatter_03( ):
   '''Multiple before, after, opening, closing format correctly on Container.'''

   t = Container(Note(1, (1, 4))*4)
   t.formatter.before.append('before1')
   t.formatter.before.append('before2')
   t.formatter.after.append('after1')
   t.formatter.after.append('after2')
   t.formatter.opening.append('opening1')
   t.formatter.opening.append('opening2')
   t.formatter.closing.append('closing1')
   t.formatter.closing.append('closing2')

   r'''before1
   before2
   {
   opening1
   opening2
           cs'4
           cs'4
           cs'4
           cs'4
   closing1
   closing2
   }
   after1
   after2'''

   assert t.format == "before1\nbefore2\n{\nopening1\nopening2\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\nclosing1\nclosing2\n}\nafter1\nafter2"


def test_container_formatter_04( ):
   '''Containers do not have left or right.'''

   t = Container(Note(1, (1, 4))*4)

   assert raises(AttributeError, "t.formatter.left.append('left')")
   assert raises(AttributeError, "t.formatter.right.append('right')")
