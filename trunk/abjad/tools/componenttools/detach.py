from abjad.tools import check
from abjad.tools.spannertools.withdraw_from_contained import \
   _withdraw_from_contained


def detach(components):
   r'''Remove arbitrary `components` and children of `components` 
   from score. ::

      abjad> score = Voice(construct.run(2))
      abjad> score.insert(1, Container(construct.run(2)))
      abjad> pitchtools.diatonicize(score)
      abjad> Beam(score.leaves)
      abjad> Glissando(score.leaves)

   ::

      abjad> f(score)
      \new Voice {
         c'8 [ \glissando
         {
            d'8 \glissando
            e'8 \glissando
         }
         f'8 ]
      }

   Examples refer to the score above.

   Remove one leaf from score::
      
      abjad> componenttools.detach(score.leaves[1:2])
      (Note(d', 8),)
      
   ::
      
      abjad> f(score)
      \new Voice {
         c'8 [ \glissando
         {
            e'8 \glissando
         }
         f'8 ]
      }

   Remove contiguous leaves from score::

      abjad> result = componenttools.detach(score.leaves[:2])
      (Note(c', 8), Note(d', 8))

   ::

      abjad> f(score)
      \new Voice {
         {
            e'8 [ \glissando
         }
         f'8 ]
      }

   Remove noncontiguous leaves from score::

      abjad> componenttools.detach([score.leaves[0], score.leaves[2]])
      [Note(c', 8), Note(e', 8)]
      
   ::
      
      abjad> f(score)
      \new Voice {
         {
            d'8 [ \glissando
         }
         f'8 ]
      }

   Remove container from score::

      abjad> result = componenttools.detach(score[1:2])
      abjad> result
      [{d'8, e'8}]
      
   ::
      
      abjad> f(score)
      \new Voice {
         c'8 [ \glissando
         f'8 ]
      }

   Withdraw `components` and children of `components` from spanners.

   Return either tuple or list of `components` and children of `components`.

   .. todo:: regularize return value of function.

   .. note:: rename to ``componenttools.remove_components_from_score_deep( )``.
   '''

   check.assert_components(components)
   for component in components:
      component.parentage._cut( )
      _withdraw_from_contained([component])
   return components
