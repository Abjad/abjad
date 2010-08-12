from abjad import *


def test_BeamSpanner_public_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = BeamSpanner(t.leaves[ : 4])
   assert isinstance(beam, BeamSpanner)
   assert len(beam.components) == 4
   for x in t[ : 4]:
      assert x.beam.spanned
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   #assert len(t.spanners) == 1
   assert len(t.spanners.contained) == 1
