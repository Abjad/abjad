from abjad import *


def test_NamedPitch__init_empty_01( ):
   '''Init empty.'''

   p = pitchtools.NamedPitch( )

   assert p.diatonic_pitch_number == None
   assert p.degree == None
   assert p.format == ''
   assert p.letter == None
   assert p.name == None
   assert p.number == None
   assert p.octave == None
   assert p.pitch_class == None
   assert p.ticks == None
