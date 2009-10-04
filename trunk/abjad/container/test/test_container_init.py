from abjad import *


def test_container_init_01( ):
   '''Abjad allows empty containers.'''

   t = Container([ ])

   assert t.duration.contents == Rational(0)
   assert t.duration.prolated == Rational(0)
   assert len(t) == 0
