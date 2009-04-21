from abjad.tools.split._at_index import _at_index as split__at_index


def unfractured_at_index(container, i):
   r'''Split container in two just before index i.
      Compare with split.container_fractured( ).
      Special spanner management to leave all spanners in tact.
      Preserve parentage, if any.
      Resize resizable containers.
      Preserve container multiplier, if any.
      Preserve meter denominator, if any.

      Example of splitting binary measure, leaving spanners in tact:

      t = Voice(RigidMeasure((3, 8), construct.run(3)) * 2)
      pitchtools.diatonicize(t)
      p = Beam(t[:])

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
                 
      split.container_unfractured(t[1], 1)

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
      }'''

   return split__at_index(container, i, spanners = 'unfractured')
