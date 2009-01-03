from abjad import *
from py.test import raises


def test_grob_handling_01( ):
   '''Leaf override without context promotion.'''
   t = Note(0, (1, 4))
   t.clef.color = 'red'
   assert t.format == "\\once \\override Clef #'color = #red\nc'4"
   r'''
   \once \override Clef #'color = #red
   c'4
   '''


def test_grob_handling_02( ):
   '''Leaf override with context promotion.'''
   t = Note(0, (1, 4))
   t.clef.color = 'red'
   t.clef.promote('color', 'Staff')
   assert t.format == "\\once \\override Staff.Clef #'color = #red\nc'4"
   r'''
   \once \override Staff.Clef #'color = #red
   c'4
   '''


def test_grob_handling_03( ):
   '''Context promotion before assignment raises an exception.'''
   t = Note(0, (1, 4))
   assert raises(AttributeError, "t.clef.promote('color', 'Staff')")


def test_grob_handling_04( ):
   '''Context override automatically includes context specification;
      context override omits \once frequency indicator.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.clef.color = 'red'
   assert t.format == "\\new Staff {\n\t\\override Staff.Clef #'color = #red\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"
   r'''
   \new Staff {
      \override Staff.Clef #'color = #red
      c'4
      c'4
      c'4
      c'4
      c'4
      c'4
      c'4
      c'4
   }
   '''
