from abjad import *


def test_NamedPitchClass___init___01( ):

   assert tonalharmony.NamedPitchClass('c').name == 'c'
   assert tonalharmony.NamedPitchClass('cs').name == 'cs'
   assert tonalharmony.NamedPitchClass('cf').name == 'cf'
   assert tonalharmony.NamedPitchClass('cqs').name == 'cqs'
   assert tonalharmony.NamedPitchClass('cqf').name == 'cqf'
