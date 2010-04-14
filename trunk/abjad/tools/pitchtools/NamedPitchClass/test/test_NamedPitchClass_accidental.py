from abjad import *


def test_NamedPitchClass_accidental_01( ):
   
   assert pitchtools.NamedPitchClass('c').accidental.alphabetic_string == ''
   assert pitchtools.NamedPitchClass('cqs').accidental.alphabetic_string == 'qs'
   assert pitchtools.NamedPitchClass('cqf').accidental.alphabetic_string == 'qf'
   assert pitchtools.NamedPitchClass('cs').accidental.alphabetic_string == 's'
   assert pitchtools.NamedPitchClass('cf').accidental.alphabetic_string == 'f'
   assert pitchtools.NamedPitchClass('ctqs').accidental.alphabetic_string == \
      'tqs'
   assert pitchtools.NamedPitchClass('ctqf').accidental.alphabetic_string == \
      'tqf'
   assert pitchtools.NamedPitchClass('css').accidental.alphabetic_string == 'ss'
   assert pitchtools.NamedPitchClass('cff').accidental.alphabetic_string == 'ff'
