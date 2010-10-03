from abjad import *


def test_NamedPitch__init_by_number_01( ):
   '''Init by number.'''

   p = pitchtools.NamedPitch(13)

   assert p.diatonic_pitch_number == 7
   assert p.format == "cs''"
   assert p.letter == 'c'
   assert p.name == 'cs'
   assert p.number == 13
   assert p.octave == 5
   assert p.pitch_class == pitchtools.NumericPitchClass(1)
   assert p.ticks == "''"
