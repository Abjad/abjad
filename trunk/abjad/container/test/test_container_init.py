from abjad import *


def test_container_empty_01( ):
   '''Abjad allows empty containers.'''

   t = Container([ ])

   assert t.duration.contents == Rational(0)
   assert t.duration.prolated == Rational(0)
   ## TODO: Eliminate public Container or format as { } ##
   #assert t.format == ''
   assert len(t) == 0
