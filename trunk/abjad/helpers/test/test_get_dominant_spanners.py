from abjad.helpers.get_dominant_spanners import _get_dominant_spanners
from abjad import *


def test_get_dominant_spanners_01( ):
   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   dominant_spanners = _get_dominant_spanners(t[:])
   assert b1 not in dominant_spanners
   assert b2 not in dominant_spanners
   assert crescendo in dominant_spanners


def test_get_dominant_spanners_02( ):
   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   dominant_spanners = _get_dominant_spanners(t[0:1])
   assert b1 in dominant_spanners
   assert b2 not in dominant_spanners
   assert crescendo in dominant_spanners
