from abjad import *


def test_Pitch__init_by_reference_01( ):
   '''Init by reference.'''

   r = Pitch('df', 5)
   p = Pitch(r)

   assert repr(p) == "Pitch(df, 5)"
   assert p.altitude == 8
   assert p.degree == 2
   assert p.format == "df''"
   assert p.letter == 'd'
   assert p.name == 'df'
   assert p.number == 13
   assert p.octave == 5
   assert p.pair == ('df', 5)
   assert p.pc == pitchtools.PitchClass(1)
   assert p.ticks == "''"
