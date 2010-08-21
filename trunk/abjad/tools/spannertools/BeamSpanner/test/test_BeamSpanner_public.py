from abjad import *


def test_BeamSpanner_public_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = spannertools.BeamSpanner(t.leaves[ : 4])
   assert isinstance(beam, spannertools.BeamSpanner)
   assert len(beam.components) == 4
   for x in t[:4]:
      #assert x.beam.spanned
      assert beamtools.is_component_with_beam_spanner_attached(x)
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   #assert len(t.spanners.contained) == 1
   assert len(spannertools.get_all_spanners_attached_to_any_improper_child_of_component(t)) == 1
