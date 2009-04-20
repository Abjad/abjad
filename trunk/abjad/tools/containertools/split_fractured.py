from abjad.tools.containertools._split_general import _split_general


def split_fractured(container, i):
   r'''Splits container in two at given index position.
      Compare with :func:`split_fractured( )`.

      Both functions break container just before index.
      However, ``containertools.split_unfractured( )`` *preserves* spanners.
      And ``containertools.split_fractured( )`` *fractures* spanners.

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

         left, right = containertools.split_fractured(tuplet, 1)

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

   return _split_general(container, i, spanners = 'fractured')
