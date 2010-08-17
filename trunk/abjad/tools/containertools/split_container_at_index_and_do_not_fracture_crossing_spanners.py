from abjad.tools.componenttools._split_component_at_index import _split_component_at_index


def split_container_at_index_and_do_not_fracture_crossing_spanners(container, index):
   r'''Split `container` at `index`. 
   Leave spanners untouched, resize resizable containers, 
   preserve container multiplier, preserve meter denominator.
   Return split parts. ::

      abjad> t = Voice(RigidMeasure((3, 8), notetools.make_repeated_notes(3)) * 2)
      abjad> macros.diatonicize(t)
      abjad> p = spannertools.BeamSpanner(t[:])
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

   .. versionchanged:: 1.1.2
      renamed ``split.unfractured_at_index( )`` to
      ``containertools.split_container_at_index_and_do_not_fracture_crossing_spanners( )``.
   '''
   
   return _split_component_at_index(container, index, spanners = 'unfractured')
