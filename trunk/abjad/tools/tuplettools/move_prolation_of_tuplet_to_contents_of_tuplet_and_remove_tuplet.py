from abjad.tools import componenttools
from abjad.components._Tuplet import _Tuplet


def move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet(tuplet):
   r'''Scale ``tuplet`` contents and then bequeath in-score \
   position of ``tuplet`` to contents.

   Return orphaned ``tuplet`` emptied of all contents. ::

      abjad> t = Staff(FixedDurationTuplet((3, 8), macros.scale(2)) * 2)
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

      abjad> tuplettools.move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet(t[0])
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

   .. versionchanged:: 1.1.2
      renamed ``tuplettools.subsume( )`` to
      ``tuplettools.move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet( )``.
   '''

   assert isinstance(tuplet, _Tuplet)
   from abjad.tools import containertools
   
   containertools.scale_contents_of_container(tuplet, tuplet.duration.multiplier)
   componenttools.move_parentage_and_spanners_from_components_to_components([tuplet], tuplet[:])

   return tuplet
