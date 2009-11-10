from abjad.tuplet import _Tuplet


def augmentation_to_diminution(tuplet):
   '''.. versionadded:: 1.1.2

   Multiply the written duration of the leaves in `tuplet` 
   by the least power of 2 necessary to diminshed `tuplet`. ::

      abjad> tuplet = FixedDurationTuplet((2, 4), construct.scale(3))
      abjad> tuplet
      FixedDurationTuplet(1/2, [c'8, d'8, e'8])
      abjad> tuplettools.augmentation_to_diminution(tuplet)
      FixedDurationTuplet(1/2, [c'4, d'4, e'4])      

   .. todo:: make work with nested tuplets.
   '''

   if not isinstance(tuplet, _Tuplet):
      raise TypeError('must be tuplet.')

   while not tuplet.duration.diminution:
      for leaf in tuplet.leaves:
         leaf.duration.written *= 2

   return tuplet
