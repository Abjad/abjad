from abjad import *


def test_NamedPitch_apply_accidental_01( ):

   assert pitchtools.NamedPitch('cs', 4).apply_accidental('sharp') == pitchtools.NamedPitch('css', 4)
   assert pitchtools.NamedPitch('cs', 4).apply_accidental('flat') == pitchtools.NamedPitch('c', 4)
   assert pitchtools.NamedPitch('cs', 4).apply_accidental('natural') == pitchtools.NamedPitch('cs', 4)
   assert pitchtools.NamedPitch('cs', 4).apply_accidental('quarter sharp') == pitchtools.NamedPitch('ctqs', 4)
