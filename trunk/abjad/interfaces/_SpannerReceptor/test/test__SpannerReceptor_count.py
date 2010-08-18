from abjad import *


def test__SpannerReceptor_count_01( ):
   '''Return 0 when no spanners attach.'''
   
   t = Staff(macros.scale(4))
   assert t[0].beam.count == 0
   assert t[0].dynamics.count == 0
   #assert t[0].glissando.count == 0
   assert len(t[0].spanners.get_all_attached_spanners_of_type(spannertools.GlissandoSpanner)) == 0
   assert t[0].tie.count == 0


def test__SpannerReceptor_count_02( ):
   '''Return 1 when one spanner attaches.'''
   
   t = Staff(macros.scale(4))
   spannertools.CrescendoSpanner(t[:])
   assert t[0].beam.count == 0
   assert t[0].dynamics.count == 1
   #assert t[0].glissando.count == 0
   assert len(t[0].spanners.get_all_attached_spanners_of_type(spannertools.GlissandoSpanner)) == 0
   assert t[0].tie.count == 0
