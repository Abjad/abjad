def sum_prolated(components):
   r'''Sum of ``component.duration.prolated`` for each ``component`` in  ``components``.

      Example::

         abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))
         abjad> print t.format

         \times 2/3 {
            c'8
            d'8
            e'8
         }

         abjad> durtools.sum_prolated(t[:])
         Rational(1, 4)'''

   assert isinstance(components, list)
   return sum([component.duration.prolated for component in components])
