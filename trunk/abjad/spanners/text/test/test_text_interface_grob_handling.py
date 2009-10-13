from abjad import *


def test_text_interface_grob_handling_01( ):
   '''
   Text override on leaf without context promotion.
   '''

   t = Note(0, (1, 4))
   t.text.color = 'red'

   r'''
   \once \override TextScript #'color = #red
   c'4
   '''

   assert t.format == "\\once \\override TextScript #'color = #red\nc'4"


def test_text_interface_grob_handling_02( ):
   '''
   Text override on leaf with context promotion.
   '''

   t = Note(0, (1, 4))
   t.text.color = 'red'
   overridetools.promote(t.text, 'color', 'Staff')

   r'''
   \once \override Staff.TextScript #'color = #red
   c'4
   '''
   
   assert t.format == "\\once \\override Staff.TextScript #'color = #red\nc'4"


def test_text_interface_grob_handling_03( ):
   '''
   Override text on context.
   '''

   t = Staff(construct.scale(4))
   t.text.color = 'red'

   r'''
      \new Staff \with {
           \override TextScript #'color = #red
   } {
           c'8
           d'8
           e'8
           f'8
   }   
   '''

   assert t.format == "\\new Staff \\with {\n\t\\override TextScript #'color = #red\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_text_interface_grob_handling_04( ):
   '''Clear all overrides.
   '''

   t = Note(0, (1, 4))
   t.text.color = 'red'
   t.text.size = 4
   #t.text.clear( )
   overridetools.clear_all(t.text)

   assert t.format == "c'4"
