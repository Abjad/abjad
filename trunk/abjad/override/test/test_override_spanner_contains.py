from abjad import *


def test_override_spanner_contains_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   override = Override(t[ : 4], 'Beam', 'positions', (8, 8))
   for x in t[ : 4]:
      assert x in override.components
