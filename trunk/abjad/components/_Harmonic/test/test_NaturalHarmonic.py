from abjad import *


def test_NaturalHarmonic_01( ):

   t = NaturalHarmonic(10, (1, 4))

   r'''
   \once \override NoteHead #'style = #'harmonic
   bf'4
   '''
   
   assert t.pitch == NamedPitch(10)
   assert t.format == "\\once \\override NoteHead #'style = #'harmonic\nbf'4"
