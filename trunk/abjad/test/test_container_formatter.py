from abjad import *
from py.test import raises

def test_container_formatter_01( ):
   '''before, after, opening, closing format correctly on Sequential.'''
   t = Sequential(Note(1, (1, 4))*4)
   t.formatter.before.append('before')
   t.formatter.after.append('after')
   t.formatter.opening.append('opening')
   t.formatter.closing.append('closing')
   assert t.format == "before\n{\nopening\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\nclosing\n}\nafter"
   '''
   before
   {
   opening
           cs'4
           cs'4
           cs'4
           cs'4
   closing
   }
   after
   '''

def test_container_formatter_02( ):
   '''before, after, opening, closing format correctly on Parallel.'''
   t = Parallel(Note(1, (1, 4))*4)
   t.formatter.before.append('before')
   t.formatter.after.append('after')
   t.formatter.opening.append('opening')
   t.formatter.closing.append('closing')
   assert t.format == "before\n<<\nopening\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\nclosing\n>>\nafter"
   '''
   before
   <<
   opening
           cs'4
           cs'4
           cs'4
           cs'4
   closing
   >>
   after
   '''

def test_container_formatter_03( ):
   '''Containers do not have left or right.'''
   t = Sequential(Note(1, (1, 4))*4)
   assert raises(AttributeError, "t.formatter.left.append('left')")
   assert raises(AttributeError, "t.formatter.right.append('right')")
