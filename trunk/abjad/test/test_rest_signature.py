from abjad import *


def test_rest_signature_01( ):
   '''Rest signature returns a written duration pair.'''
   t = Rest((1, 4))
   assert t.signature == ((1, 4), )


def test_rest_signature_02( ):
   '''Rests with like written duration test true 
      under signature comparison.'''
   t1 = Rest((1, 4))
   t2 = Rest((1, 4))
   assert t1.signature == t2.signature
