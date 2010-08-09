from abjad import *


def test_pitchtools_is_pitch_name_01( ):

   assert pitchtools.is_pitch_name('c')
   assert pitchtools.is_pitch_name('cs')
   assert pitchtools.is_pitch_name('css')
   assert pitchtools.is_pitch_name('cqs')
   assert pitchtools.is_pitch_name('ctqs')
   assert not pitchtools.is_pitch_name('foo')
