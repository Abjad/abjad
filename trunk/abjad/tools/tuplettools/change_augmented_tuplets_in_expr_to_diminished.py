from abjad.components import Tuplet


def change_augmented_tuplets_in_expr_to_diminished(tuplet):
   '''.. versionadded:: 1.1.2

   Multiply the written duration of the leaves in `tuplet` 
   by the least power of 2 necessary to diminshed `tuplet`. ::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 4), macros.scale(3))
      abjad> tuplet
      tuplettools.FixedDurationTuplet(1/2, [c'8, d'8, e'8])
      abjad> tuplettools.change_augmented_tuplets_in_expr_to_diminished(tuplet)
      tuplettools.FixedDurationTuplet(1/2, [c'4, d'4, e'4])      

   .. todo:: make work with nested tuplets.

   .. versionchanged:: 1.1.2
      renamed ``tuplettools.augmentation_to_diminution( )`` to
      ``tuplettools.change_augmented_tuplets_in_expr_to_diminished( )``.
   '''

   if not isinstance(tuplet, Tuplet):
      raise TypeError('must be tuplet.')

   while not tuplet.duration.is_diminution:
      for leaf in tuplet.leaves:
         leaf.duration.written *= 2

   return tuplet
