from abjad import *


def test_NamedChromaticPitchClass_accidental_01( ):
   
   assert pitchtools.NamedChromaticPitchClass('c').accidental.alphabetic_string == ''
   assert pitchtools.NamedChromaticPitchClass('cqs').accidental.alphabetic_string == 'qs'
   assert pitchtools.NamedChromaticPitchClass('cqf').accidental.alphabetic_string == 'qf'
   assert pitchtools.NamedChromaticPitchClass('cs').accidental.alphabetic_string == 's'
   assert pitchtools.NamedChromaticPitchClass('cf').accidental.alphabetic_string == 'f'
   assert pitchtools.NamedChromaticPitchClass('ctqs').accidental.alphabetic_string == \
      'tqs'
   assert pitchtools.NamedChromaticPitchClass('ctqf').accidental.alphabetic_string == \
      'tqf'
   assert pitchtools.NamedChromaticPitchClass('css').accidental.alphabetic_string == 'ss'
   assert pitchtools.NamedChromaticPitchClass('cff').accidental.alphabetic_string == 'ff'
