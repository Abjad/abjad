from abjad.helpers.make_orphan_components import _make_orphan_components
from abjad import *


def test_make_orphan_components_01( ):
   t = Staff(scale(4))
   components = _make_orphan_components(t[:])

   assert len(t) == 0
   assert len(components) == 4 


def test_make_orphan_components_02( ):
   t = _make_orphan_components([ ])
   assert t == [ ]
