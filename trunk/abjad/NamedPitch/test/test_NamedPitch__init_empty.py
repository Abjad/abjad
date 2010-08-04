from abjad import *


def test_NamedPitch__init_empty_01( ):
   '''Init empty.'''

   p = NamedPitch( )

   assert p.altitude == None
   assert p.degree == None
   assert p.format == ''
   assert p.letter == None
   assert p.name == None
   assert p.number == None
   assert p.octave == None
   assert p.pair == None
   assert p.pc == None
   assert p.ticks == None
