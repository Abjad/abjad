from abjad import *


def test_Container___init____01( ):
   '''Abjad allows empty containers.'''

   t = Container([ ])

   assert t.duration.contents == Fraction(0)
   assert t.duration.prolated == Fraction(0)
   assert len(t) == 0
