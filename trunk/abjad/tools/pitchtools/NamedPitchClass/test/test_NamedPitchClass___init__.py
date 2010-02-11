from abjad import *


def test_NamedPitchClass___init___01( ):

   assert pitchtools.NamedPitchClass('c').name == 'c'
   assert pitchtools.NamedPitchClass('cs').name == 'cs'
   assert pitchtools.NamedPitchClass('cf').name == 'cf'
   assert pitchtools.NamedPitchClass('cqs').name == 'cqs'
   assert pitchtools.NamedPitchClass('cqf').name == 'cqf'
