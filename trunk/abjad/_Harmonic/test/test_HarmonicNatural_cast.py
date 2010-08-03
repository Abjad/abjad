from abjad import *


def test_HarmonicNatural_cast_01( ):
   '''It is possible to cast notes into natural harmonics.'''

   t = Staff(macros.scale(4))
   HarmonicNatural(t[1])

   r'''
   \new Staff {
           c'8
           \once \override NoteHead #'style = #'harmonic
           d'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8\n\t\\once \\override NoteHead #'style = #'harmonic\n\td'8\n\te'8\n\tf'8\n}"
