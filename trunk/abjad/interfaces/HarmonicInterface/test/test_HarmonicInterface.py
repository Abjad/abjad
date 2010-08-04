from abjad import *


def test_HarmonicInterface_01( ):
   '''Add a natural harmonic.'''
   t = Note(0, (1, 4))
   t.harmonic.natural = True
   assert t.format == "c'4 \\flageolet"


def test_HarmonicInterface_02( ):
   '''Add and then remove natural harmonic.'''
   t = Note(0, (1, 4))
   t.harmonic.natural = True
   t.harmonic.natural = False
   assert t.format == "c'4"
