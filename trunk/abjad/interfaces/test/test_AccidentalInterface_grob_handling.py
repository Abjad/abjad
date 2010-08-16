from abjad import *


def test_AccidentalInterface_grob_handling_01( ):
   '''AccidentalInterface handles the LilyPond Accidental grob.
   '''

   t = Staff(macros.scale(4))
   t.override.accidental.color = 'red'

   r'''
   \new Staff \with {
           \override Accidental #'color = #red
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''
  
   assert t.format == "\\new Staff \\with {\n\t\\override Accidental #'color = #red\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_AccidentalInterface_grob_handling_02( ):
   '''
   AccidentalInterface handles the LilyPond Accidental grob.
   '''

   t = Staff(macros.scale(4))
   t[1].override.accidental.color = 'red'

   r'''
   \new Staff {
           c'8
           \once \override Accidental #'color = #red
           d'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8\n\t\\once \\override Accidental #'color = #red\n\td'8\n\te'8\n\tf'8\n}"
