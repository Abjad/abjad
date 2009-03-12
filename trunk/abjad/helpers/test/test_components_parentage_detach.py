from abjad.helpers.are_orphan_components import _are_orphan_components
from abjad import *


def test_components_parentage_detach_01( ):
   '''Detach parent from Abjad components at top level of list.'''

   t = Staff([Voice(scale(4))])
   v = t[0]
   notes = v[:]

   components_parentage_detach(v[:], level = 'top')

   assert _are_orphan_components(notes)


def test_components_parentage_detach_02( ):
   '''Detach parent from Abjad components at all levels of list.'''

   t = Staff([Voice(scale(4))])
   v = t[0]
   notes = v[:]

   components_parentage_detach([t], level = 'all')

   from abjad.component.component import _Component
   assert _are_orphan_components(list(iterate(t, _Component)))
