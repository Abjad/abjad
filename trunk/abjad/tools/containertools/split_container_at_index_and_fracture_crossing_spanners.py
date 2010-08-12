from abjad.tools.componenttools._split_component_at_index import _split_component_at_index


def split_container_at_index_and_fracture_crossing_spanners(container, index):
   r'''Split `container` at `index`. Fracture spanners,
   create two new copies of `container`, empty `container`
   of original contents.
   Return split parts. ::

      abjad> t = Voice(FixedDurationTuplet((2, 8), notetools.make_repeated_notes(3)) * 2)
      abjad> tuplet = t[1]
      abjad> macros.diatonicize(t)
      abjad> BeamSpanner(t[:])
      abjad> f(t)
      \new Voice {
              \times 2/3 {
                      c'8 [
                      d'8
                      e'8
              }
              \times 2/3 {
                      f'8
                      g'8
                      a'8 ]
              }
      }

   ::

      abjad> left, right = split.container_fractured(tuplet, 1)
      abjad> f(t)
      \new Voice {
              \times 2/3 {
                      c'8 [
                      d'8
                      e'8
              }
              \times 2/3 {
                      f'8 ]
              }
              \times 2/3 {
                      g'8 [
                      a'8 ]
              }
      }

   Function leaves leaves untouched.

   .. versionchanged:: 1.1.2
      renamed ``split.fractured_at_index( )`` to
      ``containertools.split_container_at_index_and_fracture_crossing_spanners( )``.
   '''

   return _split_component_at_index(container, index, spanners = 'fractured')
