from abjad import *


def test_staff_interface_explicit_01( ):
   '''Return first explicit *Abjad* ``Staff`` in parentage of client.
      Otherwise ``None``.'''

   t = Score([Staff(construct.scale(4))])

   r'''\new Score <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>'''

   assert t.leaves[0].staff.explicit is t[0]

   ## TODO: Add staff interface to Abjad containers. ##

#   assert t[0].staff.explicit is t[0]
#   assert t.staff.explicit is None


def test_staff_interface_explicit_02( ):
   '''Return first explicit *Abjad* ``Staff`` in parentage of client.
      Otherwise ``None``.'''

   t = Note(0, (1, 4))

   assert t.staff.explicit is None
