from abjad import *
from abjad.helpers.get_subtree_dominant_spanners_receipt import _get_subtree_dominant_spanners_receipt


def test_get_subtree_dominant_spanners_receipt_01( ):


   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
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

   receipt = _get_subtree_dominant_spanners_receipt(t[1])

   assert (beam, 1) in receipt
   assert (glissando, 0) in receipt
   assert (trill, 2) in receipt
