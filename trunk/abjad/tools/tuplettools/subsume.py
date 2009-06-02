from abjad.tuplet.tuplet import _Tuplet


def subsume(tuplet):
   r'''Scale ``tuplet`` contents and then bequeath in-score \
      position of ``tuplet`` to contents.

      Return orphaned ``tuplet`` emptied of all contents. ::

         abjad> t = Staff(FixedDurationTuplet((3, 8), construct.scale(2)) * 2)
         abjad> Beam(t.leaves)
         abjad> print t.format
         \new Staff {
                 \fraction \times 3/2 {
                         c'8 [
                         d'8
                 }
                 \fraction \times 3/2 {
                         c'8
                         d'8 ]
                 }
         }

      ::

         abjad> tuplettools.subsume(t[0])
         FixedDurationTuplet(3/8, [ ])
         abjad> print t.format
         \new Staff {
                 c'8. [
                 d'8.
                 \fraction \times 3/2 {
                         c'8
                         d'8 ]
                 }
         }


      .. note:: This function should probably be called ``scale_contents_and_bequeath( )``.

      .. note:: ``bequeath( )`` should probably be called something else, too.
   '''

   assert isinstance(tuplet, _Tuplet)
   from abjad.tools import containertools
   from abjad.tools import scoretools
   
   containertools.contents_scale(tuplet, tuplet.duration.multiplier)
   scoretools.bequeath([tuplet], tuplet[:])

   return tuplet
