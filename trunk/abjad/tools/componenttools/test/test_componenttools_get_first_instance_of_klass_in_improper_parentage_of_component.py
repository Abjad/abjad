from abjad import *


def test_componenttools_get_first_instance_of_klass_in_improper_parentage_of_component_01( ):

   t = Staff(macros.scale(4))
   
   assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
      t[0], Note) is t[0]

   assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
      t[0], Staff) is t

   assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
      t[0], Score) is None
