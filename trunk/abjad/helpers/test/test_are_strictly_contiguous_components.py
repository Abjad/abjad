from abjad.helpers.are_strictly_contiguous_components import _are_strictly_contiguous_components
from abjad import *


def test_are_strictly_contiguous_components_01( ):
   '''True for strictly contiguous leaves in voice.
      False for other time orderings of leaves in voice.'''

   t = Voice(scale(4))
   
   assert _are_strictly_contiguous_components(t.leaves)

   assert not _are_strictly_contiguous_components(
      list(reversed(t.leaves)))
   assert not _are_strictly_contiguous_components(
      t.leaves[2:] + t.leaves[:2])
   assert not _are_strictly_contiguous_components(
      t[3:4] + t[0:1])
   assert not _are_strictly_contiguous_components(
      [t] + t.leaves)


def test_are_strictly_contiguous_components_02( ):
   '''True for strictly contiguous components.'''

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

   assert _are_strictly_contiguous_components([t])
   assert _are_strictly_contiguous_components(t[:])
   assert _are_strictly_contiguous_components(t[0][:])
   assert _are_strictly_contiguous_components(t[1][:])
   assert _are_strictly_contiguous_components(t[0:1] + t[1][:])
   assert _are_strictly_contiguous_components(t[0][:] + t[1:2])
   assert _are_strictly_contiguous_components(t.leaves)


def test_are_strictly_contiguous_components_03( ):
   '''Unicorporated leaves can not be evaluated for contiguity.'''

   t = scale(4)

   assert not _are_strictly_contiguous_components(t)


def test_are_strictly_contiguous_components_04( ):
   '''Empty list returns True.'''

   t = [ ]

   assert _are_strictly_contiguous_components(t)
