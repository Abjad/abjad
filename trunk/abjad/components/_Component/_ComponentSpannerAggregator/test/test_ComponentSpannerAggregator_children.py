from abjad import *


def test_ComponentSpannerAggregator_children_01( ):
   '''Return unordered set of all spanners
      attaching to any children of self.
      Do not include spaners attaching directly to self.'''

   t = Voice(macros.scale(4))
   trill = spannertools.TrillSpanner(t)
   beam = spannertools.BeamSpanner(t[:2])
   glissando = spannertools.GlissandoSpanner(t[2:])

   r'''
   \new Voice {
      c'8 [ \startTrillSpan
      d'8 ]
      e'8 \glissando
      f'8 \stopTrillSpan
   }
   '''

   assert len(list(t.spanners.children)) == 2
   assert beam in t.spanners.children
   assert glissando in t.spanners.children


def test_ComponentSpannerAggregator_children_02( ):
   '''Return empty set when no spanners attach to children.'''

   t = Voice(macros.scale(4))

   assert t.spanners.children == set([ ])
