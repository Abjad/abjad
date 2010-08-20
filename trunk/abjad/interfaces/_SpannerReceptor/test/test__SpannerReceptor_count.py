from abjad import *


def test__SpannerReceptor_count_01( ):
   '''Return 0 when no spanners attach.'''
   
   t = Staff(macros.scale(4))
   assert len(t[0].spanners.get_all_attached_spanners_of_type(spannertools.BeamSpanner)) == 0
   assert len(t[0].spanners.get_all_attached_spanners_of_type(spannertools.HairpinSpanner)) == 0
   assert len(t[0].spanners.get_all_attached_spanners_of_type(spannertools.GlissandoSpanner)) == 0
   assert len(t[0].spanners.get_all_attached_spanners_of_type(spannertools.TieSpanner)) == 0

def test__SpannerReceptor_count_02( ):
   '''Return 1 when one spanner attaches.'''
   
   t = Staff(macros.scale(4))
   spannertools.CrescendoSpanner(t[:])
   assert len(t[0].spanners.get_all_attached_spanners_of_type(spannertools.BeamSpanner)) == 0
   assert len(t[0].spanners.get_all_attached_spanners_of_type(spannertools.HairpinSpanner)) == 1
   assert len(t[0].spanners.get_all_attached_spanners_of_type(spannertools.GlissandoSpanner)) == 0
   assert len(t[0].spanners.get_all_attached_spanners_of_type(spannertools.TieSpanner)) == 0
