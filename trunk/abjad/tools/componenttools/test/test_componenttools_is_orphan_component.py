from abjad import *


def test_componenttools_is_orphan_component_01( ):
   
   staff = Staff(macros.scale(4))

   assert componenttools.is_orphan_component(staff)
   assert not componenttools.is_orphan_component(staff[0])
   assert not componenttools.is_orphan_component(staff[1])
   assert not componenttools.is_orphan_component(staff[2])
   assert not componenttools.is_orphan_component(staff[3])
