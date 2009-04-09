from abjad.helpers.container_hew import container_hew


def container_split(container, index):
   r'''Splits container in two at given index position.
      Compare with container_hew(container, index).

      Both helpers break container just before index.
      However, container_hew( ) *preserves* spanners.
      And container_split( ) *fractures* spanners.

      Both helpers create two new copies of container.
      Both helpers empty original container of contents.

      Return split parts.
      
      Example of splitting a beamed triplet in voice:

      t = Voice(FixedDurationTuplet((2, 8), run(3)) * 2)
      tuplet = t[1]
      pitchtools.diatonicize(t)
      Beam(t[:])

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

      left, right = container_split(tuplet, 1)

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
      }'''

   return container_hew(container, index, spanners = 'fracture')
