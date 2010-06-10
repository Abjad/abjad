from abjad import *
import py.test


def test_clef_interface_grob_handling_01( ):
   '''Leaf override without context promotion.'''

   t = Note(0, (1, 4))
   t.clef.color = 'red'

   r'''
   \once \override Clef #'color = #red
   c'4
   '''

   assert t.format == "\\once \\override Clef #'color = #red\nc'4"


def test_clef_interface_grob_handling_02( ):
   '''Leaf override with context promotion.'''

   t = Note(0, (1, 4))
   t.clef.color = 'red'
   #t.clef.promote('color', 'Staff')
   overridetools.promote_attribute_to_context_on_grob_handler(t.clef, 'color', 'Staff')

   assert t.format == "\\once \\override Staff.Clef #'color = #red\nc'4"
   r'''
   \once \override Staff.Clef #'color = #red
   c'4
   '''


def test_clef_interface_grob_handling_03( ):
   '''Context promotion before assignment raises an exception.'''
   t = Note(0, (1, 4))
   #assert py.test.raises(AttributeError, "t.clef.promote('color', 'Staff')")
   assert py.test.raises(AttributeError, "overridetools.promote_attribute_to_context_on_grob_handler(t.clef, 'color', 'Staff')")


def test_clef_interface_grob_handling_04( ):
   '''
   Clef override on staff.
   '''

   t = Staff(construct.scale(4))
   t.clef.color = 'red'

   r'''
   \new Staff \with {
           \override Clef #'color = #red
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff \\with {\n\t\\override Clef #'color = #red\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
