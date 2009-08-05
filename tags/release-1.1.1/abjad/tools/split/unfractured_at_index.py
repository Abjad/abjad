from abjad.tools.split._at_index import _at_index as split__at_index


def unfractured_at_index(container, i):
   r'''Split `container` in two just before index `i`.

      * Leave spanners in tact.
      * Preserve parentage.
      * Resize resizble containers.
      * Preserve any container multiplier.
      * Preserve any meter denominator.

      Example. Split binary measure and leave spanners in tact::

         abjad> t = Voice(RigidMeasure((3, 8), construct.run(3)) * 2)
         abjad> pitchtools.diatonicize(t)
         abjad> p = Beam(t[:])
         abjad> print t.format

         \new Voice {
                         \time 3/8
                         c'8 [
                         d'8
                         e'8
                         \time 3/8
                         f'8
                         g'8
                         a'8 ]
         }
                    
         abjad> split.container_unfractured(t[1], 1)
         abjad> print t.format

         \new Voice {
                         \time 3/8
                         c'8 [
                         d'8
                         e'8
                         \time 1/8
                         f'8
                         \time 2/8
                         g'8
                         a'8 ]
         }
   
      See also:

      :doc:`split.unfracture_at_duration( ) </chapters/api/tools/split/unfractured_at_duration>`'''

   return split__at_index(container, i, spanners = 'unfractured')
