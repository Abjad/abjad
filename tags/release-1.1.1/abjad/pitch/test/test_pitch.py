from abjad import *


def test_pitch_01( ):
   '''Public interface.'''
   p = Pitch(13)
   assert repr(p) == 'Pitch(cs, 5)'
   assert p.altitude == 7
   assert p.degree == 1
   assert p.format == "cs''"
   assert p.letter == 'c'
   #assert p.lily == "cs''"
   assert p.name == 'cs'
   assert p.number == 13
   assert p.octave == 5
   assert p.pair == ('cs', 5)
   assert p.pc == 1
   assert p.ticks == "''"


def test_pitch_02( ):
   '''Public interface for enharmonic equivalent.'''
   p = Pitch('df', 5)
   assert repr(p) == 'Pitch(df, 5)'
   assert p.altitude == 8
   assert p.degree == 2
   assert p.format == "df''"
   assert p.letter == 'd'
   #assert p.lily == "df''"
   assert p.name == 'df'
   assert p.number == 13
   assert p.octave == 5
   assert p.pair == ('df', 5)
   assert p.pc == 1
   assert p.ticks == "''"
