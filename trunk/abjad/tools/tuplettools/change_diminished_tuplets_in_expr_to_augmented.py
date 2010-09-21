from abjad.components.Tuplet import _Tuplet


def change_diminished_tuplets_in_expr_to_augmented(tuplet):
   '''.. versionadded:: 1.1.2

   Divide the written duration of the leaves in `tuplet`
   by the least power of 2 necessary to augment `tuplet`. ::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> tuplet
      tuplettools.FixedDurationTuplet(1/4, [c'8, d'8, e'8])
      abjad> tuplettools.change_diminished_tuplets_in_expr_to_augmented(tuplet)
      tuplettools.FixedDurationTuplet(1/4, [c'16, d'16, e'16])

   .. todo:: make work with nested tuplets.

   .. versionchanged:: 1.1.2
      renamed ``tuplettools.diminution_to_augmentation( )`` to
      ``tuplettools.change_diminished_tuplets_in_expr_to_augmented( )``.
   '''

   if not isinstance(tuplet, _Tuplet):
      raise TypeError('must be tuplet')

   while tuplet.duration.is_diminution:
      for leaf in tuplet.leaves:
         leaf.duration.written /= 2

   return tuplet
