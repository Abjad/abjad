from abjad import *


def test_NamedPitch__init_by_number_01( ):
   '''Init by number.'''

   p = NamedPitch(13)

   assert p.altitude == 7
   assert p.degree == 1
   assert p.format == "cs''"
   assert p.letter == 'c'
   assert p.name == 'cs'
   assert p.number == 13
   assert p.octave == 5
   assert p.pair == ('cs', 5)
   assert p.pc == pitchtools.PitchClass(1)
   assert p.ticks == "''"
