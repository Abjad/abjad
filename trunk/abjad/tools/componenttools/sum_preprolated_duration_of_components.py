def sum_preprolated_duration_of_components(components):
   r'''Sum the preprolated duration of each component in `components`. ::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> componenttools.sum_preprolated_duration_of_components(tuplet[:])
      Rational(3, 8)

   Return zero on empty iterable. ::

      abjad> componenttools.sum_preprolated_duration_of_components([ ])
      Rational(0)

   Raise contiguity error on nonparent-contiguous `components`. ::

      abjad> t = Voice(tuplettools.FixedDurationTuplet((2, 8), notetools.make_repeated_notes(3)) * 2)
      abjad> macros.diatonicize(t)
      abjad> f(t)
      \new Voice {
         \times 2/3 {
            c'8
            d'8
            e'8
         }
         \times 2/3 {
            f'8
            g'8
            a'8
         }
      }
      abjad> componenttools.sum_preprolated_duration_of_components(t.leaves)
      ContiguityError

   .. versionchanged:: 1.1.2
      renamed ``componenttools.get_duration_preprolated( )`` to
      ``componenttools.sum_preprolated_duration_of_components( )``.

   .. versionchanged:: 1.1.2
      renamed ``componenttools.get_preprolated_duration_of_components( )`` to
      ``componenttools.sum_preprolated_duration_of_components( )``.
   '''

   ## sum preprolated durations
   result = sum([component.duration.preprolated for component in components])

   ## return sum
   return result
