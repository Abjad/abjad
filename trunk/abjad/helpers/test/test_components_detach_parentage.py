from abjad.helpers.are_orphan_components import _are_orphan_components
from abjad.helpers.components_detach_parentage import \
   _components_detach_parentage
from abjad import *


def test_components_detach_parentage_01( ):
   '''Detach parent from Abjad components at top level of list.
      Traverse shallowly. Do not descend into components.'''

   t = Staff([Voice(scale(4))])
   v = t[0]
   notes = v[:]

   _components_detach_parentage(v[:])

   assert _are_orphan_components(notes)
