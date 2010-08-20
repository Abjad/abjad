from abjad import *


def test__SpannerReceptor_unspan_01( ):
   '''Unspan a spanned leaf.
   '''

   t = Note(0, (1, 8))
   spannertools.BeamSpanner(t)
   #t.beam.unspan( )
   spannertools.destroy_all_spanners_attached_to_component(t, spannertools.BeamSpanner)

   r'''
   c'8
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "c'8"


def test__SpannerReceptor_unspan_02( ):
   '''Unspan an already unspanned leaf.
   '''

   t = Note(0, (1, 8))
   #t.beam.unspan( )
   spannertools.destroy_all_spanners_attached_to_component(t, spannertools.BeamSpanner)

   r'''
   c'8
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "c'8"
