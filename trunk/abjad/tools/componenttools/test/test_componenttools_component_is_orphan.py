from abjad import *


def test_componenttools_component_is_orphan_01( ):
   
   staff = Staff(macros.scale(4))

   assert componenttools.component_is_orphan(staff)
   assert not componenttools.component_is_orphan(staff[0])
   assert not componenttools.component_is_orphan(staff[1])
   assert not componenttools.component_is_orphan(staff[2])
   assert not componenttools.component_is_orphan(staff[3])
