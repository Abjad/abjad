def sum_preprolated(components):
   r'''Sum the preprolated duration of `components`.

   ::

      abjad> tuplet = FixedDurationTuplet((2, 8), construct.scale(3))
      abjad> f(tuplet)
      \times 2/3 {
         c'8
         d'8
         e'8
      }
      abjad> durtools.sum_preprolated(tuplet[:])
      Rational(3, 8)
   '''

   assert isinstance(components, list)
   return sum([component.duration.preprolated for component in components])
