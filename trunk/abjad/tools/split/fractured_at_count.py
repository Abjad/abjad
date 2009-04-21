from abjad.tools.split._at_count import _at_count as split__at_count


def fractured_at_count(container, i):
   r'''Splits container in two at given index position.
      Compare with :func:`split.container_fractured( )`.

      Both functions break container just before index.
      However, ``split.container_unfractured( )`` *preserves* spanners.
      And ``split.container_fractured( )`` *fractures* spanners.

      Both functions create two new copies of container.
      Both functions empty original container of contents.

      Return split parts.
      
      Example of splitting a beamed triplet in voice::

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

         left, right = split.container_fractured(tuplet, 1)

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

   return split__at_count(container, i, spanners = 'fractured')
