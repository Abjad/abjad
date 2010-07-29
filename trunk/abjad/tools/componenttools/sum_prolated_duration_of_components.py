def sum_prolated_duration_of_components(components):
   r'''Sum the prolated duration of `components`.

   ::

      abjad> tuplet = FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> f(tuplet)
      \times 2/3 {
         c'8
         d'8
         e'8
      }
      abjad> componenttools.sum_prolated_duration_of_components(tuplet[:])
      Rational(1, 4)

   .. versionchanged:: 1.1.2
      renamed ``durtools.sum_prolated( )`` to
      ``componenttools.sum_prolated_duration_of_components( )``.
   '''

   return sum([component.duration.prolated for component in components])
