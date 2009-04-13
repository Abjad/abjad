from abjad import *


def test_spannertools_get_dominant_between_01( ):
   '''Return Python list of (spanner, index) pairs.
      Each spanner dominates a *crack* between components.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[1:])
   trill = Trill(t.leaves)

   r'''\new Voice {
      {
         c'8 [ \startTrillSpan
         d'8
      }
      {
         e'8 \glissando
         f'8 ] \glissando
      }
      {
         g'8 \glissando
         a'8 \stopTrillSpan
      }
   }'''

   "No spanners dominate t[0:0]"

   receipt = spannertools.get_dominant_between(None, t[0])

   assert len(receipt) == 0
   assert receipt == set([ ])


def test_spannertools_get_dominant_between_02( ):
   '''Beam and trill both dominate crack at t[1:1].'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[1:])
   trill = Trill(t.leaves)

   receipt = spannertools.get_dominant_between(t[0], t[1])

   assert len(receipt) == 2
   assert (beam, 1) in receipt
   assert (trill, 2) in receipt


def test_spannertools_get_dominant_between_03( ):
   '''Glissando and trill both dominate crack at t[2:2].'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[1:])
   trill = Trill(t.leaves)

   receipt = spannertools.get_dominant_between(t[1], t[2])
   
   assert len(receipt) == 2
   assert (glissando, 1) in receipt
   assert (trill, 4) in receipt


def test_spannertools_get_dominant_between_04( ):
   '''No spanners dominate 'crack' following voice.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   beam = Beam(t[:2])
   glissando = Glissando(t[1:])
   trill = Trill(t.leaves)

   receipt = spannertools.get_dominant_between(t[2], None)
  
   assert len(receipt) == 0
   assert receipt == set([ ])
