from abjad import *


def test_NamedPitch__init_by_number_and_letter_01( ):
   '''Init by number and letter.'''

   p = pitchtools.NamedPitch(13, 'd')

   assert p.diatonic_pitch_number == 8
   assert p.degree == 2
   assert p.format == "df''"
   assert p.letter == 'd'
   assert p.name == 'df'
   assert p.number == 13
   assert p.octave == 5
   assert p.pair == ('df', 5)
   assert p.pitch_class == pitchtools.NumericPitchClass(1)
   assert p.ticks == "''"
