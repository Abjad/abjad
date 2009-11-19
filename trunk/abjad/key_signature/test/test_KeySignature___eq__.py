from abjad import *


def test_KeySignature___eq___01( ):

   ks1 = KeySignature('g', 'major')
   ks2 = KeySignature('g', 'major')
   ks3 = KeySignature('g', 'minor')

   assert ks1 == ks2
   assert not ks2 == ks3
   assert not ks3 == ks1
