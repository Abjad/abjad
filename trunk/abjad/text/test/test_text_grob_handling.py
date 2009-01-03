from abjad import *


def test_grob_handling_01( ):
   '''Grob override on leaf without context promotion.'''
   t = Note(0, (1, 4))
   t.text.color = 'red'
   assert t.format == "\\once \\override TextScript #'color = #red\nc'4"
   r'''
   \once \override TextScript #'color = #red
   c'4
   '''


def test_grob_handling_02( ):
   '''Grob override on leaf with context promotion.'''
   t = Note(0, (1, 4))
   t.text.color = 'red'
   t.text.promote('color', 'Staff')
   assert t.format == "\\once \\override Staff.TextScript #'color = #red\nc'4"
   r'''
   \once \override Staff.TextScript #'color = #red
   c'4
   '''


def test_grob_handling_03( ):
   '''Grob override on context;
      automatic context inclusion;
      no \once frequency indicator.'''
   t = Staff(Note(0, (1, 4)) * 8)
   t.text.color = 'red'
   assert t.format == "\\new Staff {\n\t\\override Staff.TextScript #'color = #red\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"
   r'''
   \new Staff { \override Staff.TextScript #'color = #red
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
      

def test_grob_handling_04( ):
   '''Clear all overrides.'''
   t = Note(0, (1, 4))
   t.text.color = 'red'
   t.text.size = 4
   t.text.clear( )
   assert t.format == "c'4"
