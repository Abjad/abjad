from abjad import *


def test_accidental_init_01( ):
   '''Accidentals can initialize from a string.'''
   t = pitchtools.Accidental('s')
   assert t == pitchtools.Accidental('s')


def test_accidental_init_02( ):
   '''Accidentals can initialize from other accidentals.'''
   t = pitchtools.Accidental(pitchtools.Accidental('s'))
   assert t == pitchtools.Accidental('s')
