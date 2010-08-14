from abjad import *


def test_OverrideNamespace___setattr___01( ):

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
