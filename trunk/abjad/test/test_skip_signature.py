from abjad import *


def test_skip_signature_01( ):
   '''Skip signature returns a written duration pair.'''
   t = Skip((1, 4))
   assert t.signature == (1, 4)


def test_skip_signature_02( ):
   '''Skips with like written duration test true 
      under signature comparison.'''
   t1 = Skip((1, 4))
   t2 = Skip((1, 4))
