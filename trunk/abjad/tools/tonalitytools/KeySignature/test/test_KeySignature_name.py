from abjad import *


def test_KeySignature_name_01( ):

   assert tonalitytools.KeySignature('e', 'major').name == 'E major'
   assert tonalitytools.KeySignature('E', 'major').name == 'E major'

   assert tonalitytools.KeySignature('e', 'minor').name == 'e minor'
   assert tonalitytools.KeySignature('E', 'minor').name == 'e minor'
