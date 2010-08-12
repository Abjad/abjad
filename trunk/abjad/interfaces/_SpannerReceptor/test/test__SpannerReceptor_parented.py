from abjad import *
import py.test


def test__SpannerReceptor_parented_01( ):
   '''Leaves are parented when spanner is attached to them.'''

   t = Staff(notetools.make_repeated_notes(4))
   b = Beam(t.leaves)

   assert not t.beam.parented
   for leaf in t.leaves:
      assert leaf.beam.parented


def test__SpannerReceptor_parented_02( ):
   '''Leaves are parented when spanner is attached to their parent.'''

   t = Staff(notetools.make_repeated_notes(4))
   b = Beam(t)

   assert t.beam.parented
   for leaf in t.leaves:
      assert leaf.beam.parented


def test__SpannerReceptor_parented_03( ):
   '''Leaves and Containers are parented when spanner is attached to 
      their grandparent and parent repsectively.'''

   t = Staff(Voice(notetools.make_repeated_notes(4)) * 2)

   assert py.test.raises(AssertionError, 'b = Beam(t)')
#   assert t.beam.parented
#   for v in t:
#      assert v.beam.parented
#   for leaf in t.leaves:
#      assert leaf.beam.parented
