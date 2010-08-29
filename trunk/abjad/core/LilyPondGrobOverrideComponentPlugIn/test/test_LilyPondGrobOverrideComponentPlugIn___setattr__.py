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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___05( ):
   '''Leaf override without context promotion.
   '''

   t = Note(0, (1, 4))
   t.override.clef.color = 'red'

   r'''
   \once \override Clef #'color = #red
   c'4
   '''

   assert t.format == "\\once \\override Clef #'color = #red\nc'4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___06( ):
   '''Leaf override with context promotion.
   '''

   t = Note(0, (1, 4))
   t.override.staff.clef.color = 'red'

   assert t.format == "\\once \\override Staff.Clef #'color = #red\nc'4"
   r'''
   \once \override Staff.Clef #'color = #red
   c'4
   '''


def test_LilyPondGrobOverrideComponentPlugIn___setattr___07( ):
   '''Clef override on staff.
   '''

   t = Staff(macros.scale(4))
   t.override.clef.color = 'red'

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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___08( ):
   '''Transparent meter on staff.'''

   t = Staff(macros.scale(4))
   t.override.time_signature.transparent = True

   r'''
   \new Staff \with {
           \override TimeSignature #'transparent = ##t
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff \\with {\n\t\\override TimeSignature #'transparent = ##t\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___09( ):
   '''(Nonpromoted) transparent meter on measure.'''

   t = Measure((4, 8), macros.scale(4))
   t.override.time_signature.transparent = True

   r'''
   {
           \override TimeSignature #'transparent = ##t
           \time 4/8
           c'8
           d'8
           e'8
           f'8
           \revert TimeSignature #'transparent
   }
   '''

   assert t.format == "{\n\t\\override TimeSignature #'transparent = ##t\n\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert TimeSignature #'transparent\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___10( ):
   '''Promoted transarent meter on measure.'''

   t = Measure((4, 8), macros.scale(4))
   t.override.staff.time_signature.transparent = True

   r'''
   {
           \override Staff.TimeSignature #'transparent = ##t
           \time 4/8
           c'8
           d'8
           e'8
           f'8
           \revert Staff.TimeSignature #'transparent
   }
   '''

   assert t.format == "{\n\t\\override Staff.TimeSignature #'transparent = ##t\n\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert Staff.TimeSignature #'transparent\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___11( ):
   '''Clear all meter overrides.'''

   t = Note(0, (1, 4))
   t.override.time_signature.color = 'red'
   t.override.time_signature.transparent = True
   del(t.override.time_signature)

   assert t.format == "c'4"
