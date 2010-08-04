from abjad import *


def test_Pitch_apply_accidental_01( ):

   assert NamedPitch('cs', 4).apply_accidental('sharp') == NamedPitch('css', 4)
   assert NamedPitch('cs', 4).apply_accidental('flat') == NamedPitch('c', 4)
   assert NamedPitch('cs', 4).apply_accidental('natural') == NamedPitch('cs', 4)
   assert NamedPitch('cs', 4).apply_accidental('quarter sharp') == NamedPitch('ctqs', 4)
