from abjad.tools.split._at_index import _at_index


def fractured_at_index(container, index):
   r'''Split `container` at `index`. Fracture spanners,
   create two new copies of `container`, empty `container`
   of original contents.
   Return split parts. ::

      abjad> t = Voice(FixedDurationTuplet((2, 8), construct.run(3)) * 2)
      abjad> tuplet = t[1]
      abjad> pitchtools.diatonicize(t)
      abjad> Beam(t[:])
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
   '''

   return _at_index(container, index, spanners = 'fractured')
