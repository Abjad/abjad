from abjad.tools.spannertools.HairpinSpanner import HairpinSpanner


class CrescendoSpanner(HairpinSpanner):
   r'''Abjad crescendo spanner that does not avoid rests::

      abjad> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")

   ::

      abjad> f(staff)
      \new Staff {
         r4
         c'8
         d'8
         e'8
         f'8
         r4
      }

   ::

      abjad> spannertools.CrescendoSpanner(staff[:], avoid_rests = False)
      CrescendoSpanner(r4, c'8, d'8, e'8, f'8, r4)

   ::

      abjad> f(staff)
      \new Staff {
         r4 \<
         c'8
         d'8
         e'8
         f'8
         r4 \!
      }

   Abjad crescendo spanner that does avoid rests::

      abjad> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")

   ::

      abjad> f(staff)
      \new Staff {
         r4
         c'8
         d'8
         e'8
         f'8
         r4
      }

   ::

      abjad> spannertools.CrescendoSpanner(staff[:], avoid_rests = True)
      CrescendoSpanner(r4, c'8, d'8, e'8, f'8, r4)

   ::

      abjad> f(staff)
      \new Staff {
         r4
         c'8 \<
         d'8
         e'8
         f'8 \!
         r4
      }

   Return crescendo spanner.
   '''

   def __init__(self, music, avoid_rests = False):
      HairpinSpanner.__init__(self, music, '<', avoid_rests)
