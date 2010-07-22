from abjad import *


def test_componenttools_get_first_instance_of_klass_in_proper_parentage_of_component_01( ):

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   
   assert componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(t[0], Staff) is t
   assert componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(t[0], Score) is None
