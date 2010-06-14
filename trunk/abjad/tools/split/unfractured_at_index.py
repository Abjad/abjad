from abjad.tools.split._at_index import _at_index


def unfractured_at_index(container, index):
   r'''Split `container` at `index`. 
   Leave spanners untouched, resize resizable containers, 
   preserve container multiplier, preserve meter denominator.
   Return split parts. ::

      abjad> t = Voice(RigidMeasure((3, 8), leaftools.make_repeated_notes(3)) * 2)
      abjad> pitchtools.diatonicize(t)
      abjad> p = Beam(t[:])
      abjad> f(t)
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

   ::
                 
      abjad> split.container_unfractured(t[1], 1)
      abjad> f(t)
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

   Function leaves leaves untouched.
   '''
   
   return _at_index(container, index, spanners = 'unfractured')
