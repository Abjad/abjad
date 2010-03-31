from abjad import *


def test_NamedPitchClass_accidental_01( ):
   
   assert pitchtools.NamedPitchClass('c').accidental == ''
   assert pitchtools.NamedPitchClass('cqs').accidental == 'qs'
   assert pitchtools.NamedPitchClass('cqf').accidental == 'qf'
   assert pitchtools.NamedPitchClass('cs').accidental == 's'
   assert pitchtools.NamedPitchClass('cf').accidental == 'f'
   assert pitchtools.NamedPitchClass('ctqs').accidental == 'tqs'
   assert pitchtools.NamedPitchClass('ctqf').accidental == 'tqf'
   assert pitchtools.NamedPitchClass('css').accidental == 'ss'
   assert pitchtools.NamedPitchClass('cff').accidental == 'ff'
