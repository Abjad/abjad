from abjad import *


def test_HarmonicNatural_01( ):

   t = HarmonicNatural(10, (1, 4))

   r'''
   \once \override NoteHead #'style = #'harmonic
   bf'4
   '''
   
   assert t.pitch == Pitch(10)
   assert t.format == "\\once \\override NoteHead #'style = #'harmonic\nbf'4"
