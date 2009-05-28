def sum_preprolated(components):
   r'''Sum of ``component.duration.preprolated`` for each ``component`` in  ``components``.

      Example::

         abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))
         abjad> print t.format

         \times 2/3 {
            c'8
            d'8
            e'8
         }

         abjad> durtools.sum_preprolated(t[:])
         Rational(3, 8)'''

   assert isinstance(components, list)
   return sum([component.duration.preprolated for component in components])
