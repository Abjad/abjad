def sum_prolated(components):
   r'''Sum of prolated duration of each component in `components`.

   ::

      abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))
      abjad> print t.format
      \times 2/3 {
         c'8
         d'8
         e'8
      }
      abjad> durtools.sum_prolated(t[:])
      Rational(1, 4)
   '''

   return sum([component.duration.prolated for component in components])
