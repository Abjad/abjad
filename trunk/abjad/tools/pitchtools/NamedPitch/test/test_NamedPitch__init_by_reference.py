from abjad import *


def test_NamedPitch__init_by_reference_01( ):
   '''Init by reference.'''

   r = pitchtools.NamedPitch('df', 5)
   p = pitchtools.NamedPitch(r)

   assert p.diatonic_pitch_number == 8
   assert p.degree == 2
   assert p.format == "df''"
   assert p.letter == 'd'
   assert p.name == 'df'
   assert p.number == 13
   assert p.octave == 5
   assert p.pitch_class == pitchtools.NumericPitchClass(1)
   assert p.ticks == "''"
