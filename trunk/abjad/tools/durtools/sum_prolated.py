def sum_prolated(components):
   r'''Sum the prolated duration of `components`.

   ::

      abjad> tuplet = FixedDurationTuplet((2, 8), construct.scale(3))
      abjad> f(tuplet)
      \times 2/3 {
         c'8
         d'8
         e'8
      }
      abjad> durtools.sum_prolated(tuplet[:])
      Rational(1, 4)
   '''

   return sum([component.duration.prolated for component in components])
