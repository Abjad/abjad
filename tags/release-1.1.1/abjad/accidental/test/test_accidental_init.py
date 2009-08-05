from abjad import *


def test_accidental_init_01( ):
   '''Accidentals can initialize from a string.'''
   t = Accidental('s')
   assert t == Accidental('s')


def test_accidental_init_02( ):
   '''Accidentals can initialize from other accidentals.'''
   t = Accidental(Accidental('s'))
   assert t == Accidental('s')
