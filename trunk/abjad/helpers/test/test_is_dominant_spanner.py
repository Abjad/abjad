from abjad.helpers.is_dominant_spanner import _is_dominant_spanner
from abjad import *


def test_is_dominant_spanner_01( ):
   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t[:])

   assert not _is_dominant_spanner(b1, t[:])
   assert not _is_dominant_spanner(b2, t[:])
   assert _is_dominant_spanner(crescendo, t[:])


def test_is_dominante_spanner_02( ):
   t = Staff(scale(4))
   b1 = Beam(t[:])

   assert not _is_dominant_spanner(b1, [ ])
