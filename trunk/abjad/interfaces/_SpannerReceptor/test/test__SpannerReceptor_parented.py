from abjad import *
import py.test


def test__SpannerReceptor_parented_01( ):
   '''Leaves are parented when spanner is attached to them.'''

   t = Staff(notetools.make_repeated_notes(4))
   b = spannertools.BeamSpanner(t.leaves)

   #assert not t.beam.parented
   assert not spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(
      t, spannertools.BeamSpanner)
   for leaf in t.leaves:
      #assert leaf.beam.parented
      assert spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(
         leaf, spannertools.BeamSpanner)


def test__SpannerReceptor_parented_02( ):
   '''Leaves are parented when spanner is attached to their parent.'''

   t = Staff(notetools.make_repeated_notes(4))
   b = spannertools.BeamSpanner(t)

   #assert t.beam.parented
   assert spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(
      t, spannertools.BeamSpanner)
   for leaf in t.leaves:
      #assert leaf.beam.parented
      assert spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(
         t, spannertools.BeamSpanner)


def test__SpannerReceptor_parented_03( ):

   t = Staff(Voice(notetools.make_repeated_notes(4)) * 2)

   assert py.test.raises(AssertionError, 'b = spannertools.BeamSpanner(t)')
