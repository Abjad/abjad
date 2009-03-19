from abjad.helpers.test_components import _test_components
from abjad import *


def test_test_components_strict_score_01( ):
   '''True for strictly contiguous leaves in voice.
      False for other time orderings of leaves in voice.'''

   t = Voice(scale(4))
   
   assert _test_components(t.leaves, contiguity = 'strict', share = 'score')

   assert not _test_components(list(reversed(t.leaves)), 
      contiguity = 'strict', share = 'score')
   assert not _test_components(t.leaves[2:] + t.leaves[:2], 
      contiguity = 'strict', share = 'score')
   assert not _test_components(t[3:4] + t[0:1], 
      contiguity = 'strict', share = 'score')
   assert not _test_components([t] + t.leaves, 
      contiguity = 'strict', share = 'score')


def test_test_components_strict_score_02( ):
   '''True for unincorporated components.
      True across container boundaries.'''

   t = Voice(Sequential(run(2)) * 2)
   diatonicize(t)

   r'''\new Voice {
           {
                   c'8
                   d'8
           }
           {
                   e'8
                   f'8
           }
   }'''

   assert _test_components([t], contiguity = 'strict', share = 'score')
   assert _test_components(t[:], contiguity = 'strict', share = 'score')
   assert _test_components(t[0][:], contiguity = 'strict', share = 'score')
   assert _test_components(t[1][:], contiguity = 'strict', share = 'score')
   assert _test_components(t.leaves, contiguity = 'strict', share = 'score')


def test_test_components_strict_score_03( ):
   '''True for orphan components when allow_orphans is True.
      False for orphan components when allow_orphans is False.'''

   t = scale(4)

   assert _test_components(t, contiguity = 'strict', share = 'score')
   assert not _test_components(t, allow_orphans = False, 
      contiguity = 'strict', share = 'score')


def test_test_components_strict_score_04( ):
   '''Empty list returns True.'''

   t = [ ]

   assert _test_components(t, contiguity = 'strict', share = 'score')
