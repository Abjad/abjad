from abjad import *


def test_AccidentalInterface_style_01( ):
   '''AccidentalInterface.style manages LilyPond set-accidental-style.
   '''

   t = Staff(macros.scale(4))
   t.accidental.style = 'forget'

   r'''
   \new Staff {
           #(set-accidental-style 'forget)
           c'8
           d'8
           e'8
           f'8
   } 
   '''

   assert t.format == "\\new Staff {\n\t#(set-accidental-style 'forget)\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_AccidentalInterface_style_02( ):
   '''AccidentalInterface.style manages LilyPond set-accidental-style.
   '''

   t = Staff(macros.scale(4))
   t[1].accidental.style = 'forget'

   r'''
   \new Staff {
           c'8
           #(set-accidental-style 'forget)
           d'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8\n\t#(set-accidental-style 'forget)\n\td'8\n\te'8\n\tf'8\n}"
