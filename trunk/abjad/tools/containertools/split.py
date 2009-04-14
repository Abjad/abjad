from abjad.tools.containertools.hew import hew


def split(container, index):
   r'''Splits container in two at given index position.
      Compare with container.hew(container, index).

      Both functions break container just before index.
      However, container.hew( ) *preserves* spanners.
      And container.split( ) *fractures* spanners.

      Both functions create two new copies of container.
      Both functions empty original container of contents.

      Return split parts.
      
      Example of splitting a beamed triplet in voice:

      t = Voice(FixedDurationTuplet((2, 8), construct.run(3)) * 2)
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

      left, right = container.split(tuplet, 1)

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

   return hew(container, index, spanners = 'fracture')
