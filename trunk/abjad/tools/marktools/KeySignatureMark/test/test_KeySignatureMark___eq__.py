from abjad import *


def test_KeySignatureMark___eq___01( ):

   ks1 = marktools.KeySignatureMark('g', 'major')
   ks2 = marktools.KeySignatureMark('g', 'major')
   ks3 = marktools.KeySignatureMark('g', 'minor')

   assert ks1 == ks2
   assert not ks2 == ks3
   assert not ks3 == ks1
