from abjad import *


def test_LilyPondGrobOverrideComponentPlugIn___setattr___01( ):

   note = Note(0, (1, 4))
   note.override.accidental.color = 'red'
   note.override.beam.positions = (-6, -6)
   note.override.dots.thicknes = 2

   r'''
   \once \override Accidental #'color = #red
   \once \override Beam #'positions = #'(-6 . -6)
   \once \override Dots #'thicknes = #2
   c'4
   '''

   assert note.format == "\\once \\override Accidental #'color = #red\n\\once \\override Beam #'positions = #'(-6 . -6)\n\\once \\override Dots #'thicknes = #2\nc'4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___02( ):

   t = Staff(macros.scale(4))
   t.override.staff_symbol.color = 'red'

   r'''
   \new Staff \with {
           \override StaffSymbol #'color = #red
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''
 
   assert t.format == "\\new Staff \\with {\n\t\\override StaffSymbol #'color = #red\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___03( ):

   t = Staff(macros.scale(4))
   t[2].override.staff.staff_symbol.color = 'red'

   r'''
   \new Staff {
           c'8
           d'8
           \once \override Staff.StaffSymbol #'color = #red
           e'8
           f'8
   }
   '''

   t.format == "\\new Staff {\n\tc'8\n\td'8\n\t\\once \\override Staff.StaffSymbol #'color = #red\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___04( ):

   staff = Staff(macros.scale(4))
   staff.override.staff_symbol.line_positions = schemetools.SchemeVector(-4, -2, 2, 4)

   r'''
   \new Staff \with {
           \override StaffSymbol #'line-positions = #'(-4 -2 2 4)
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert staff.format == "\\new Staff \\with {\n\t\\override StaffSymbol #'line-positions = #'(-4 -2 2 4)\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
