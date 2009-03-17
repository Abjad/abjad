from abjad.helpers.are_containerized_components import _are_containerized_components
from abjad import *


def test_are_containerized_components_01( ):
   '''Leaves in voice are all containerized components.'''

   t = Voice(scale(4))
   
   assert _are_containerized_components(t.leaves)
   assert _are_containerized_components(list(reversed(t.leaves)))
   assert _are_containerized_components(t.leaves[2:] + t.leaves[:2])
   assert _are_containerized_components(t[3:4] + t[0:1])

   assert not _are_containerized_components([t] + t.leaves)


def test_are_containerized_components_02( ):
   '''False across container boundaries.'''

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

   assert not _are_containerized_components([t])

   assert _are_containerized_components(t[:])

   assert _are_containerized_components(t[0][:])
   assert _are_containerized_components(t[1][:])

   assert not _are_containerized_components(t.leaves)


def test_are_containerized_components_03( ):
   '''Unicorporated leaves are not containerized.'''

   t = scale(4)

   assert not _are_containerized_components(t)


def test_are_containerized_components_04( ):
   '''Empty list returns True.'''

   t = [ ]

   assert _are_containerized_components(t)
