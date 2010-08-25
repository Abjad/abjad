from abjad import *


def test_StaffInterface_explicit_01( ):
   '''Return first explicit Abjad ``Staff`` in parentage of client.
      Otherwise ``None``.'''

   t = Score([Staff(macros.scale(4))])

   r'''
   \new Score <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>
   '''

   #assert t.leaves[0].staff.explicit is t[0]
   #assert t[0].staff.explicit is t[0]
   #assert t.staff.explicit is None

   assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
      t.leaves[0], Staff) is t[0]
   assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
      t[0], Staff) is t[0]
   assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
      t, Staff) is None


def test_StaffInterface_explicit_02( ):
   '''Return first explicit Abjad staff in parentage of client.
   '''

   t = Note(0, (1, 4))

   #assert t.staff.explicit is None
   assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
      t, Staff) is None
