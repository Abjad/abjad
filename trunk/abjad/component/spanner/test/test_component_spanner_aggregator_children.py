from abjad import *


def test_component_spanner_aggregator_children_01( ):
   '''Return unordered set of all spanners
      attaching to any children of self.
      Do not include spaners attaching directly to self.'''

   t = Voice(construct.scale(4))
   trill = Trill(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[2:])

   r'''\new Voice {
      c'8 [ \startTrillSpan
      d'8 ]
      e'8 \glissando
      f'8 \stopTrillSpan
   }'''

   assert len(list(t.spanners.children)) == 2
   assert beam in t.spanners.children
   assert glissando in t.spanners.children


def test_component_spanner_aggregator_children_02( ):
   '''Return empty set when no spanners attach to children.'''

   t = Voice(construct.scale(4))

   assert t.spanners.children == set([ ])
