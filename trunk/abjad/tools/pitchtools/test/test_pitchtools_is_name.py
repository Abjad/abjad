from abjad import *


def test_pitchtools_is_name_01( ):

   assert pitchtools.is_name('c')
   assert pitchtools.is_name('cs')
   assert pitchtools.is_name('css')
   assert pitchtools.is_name('cqs')
   assert pitchtools.is_name('ctqs')
   assert not pitchtools.is_name('foo')
