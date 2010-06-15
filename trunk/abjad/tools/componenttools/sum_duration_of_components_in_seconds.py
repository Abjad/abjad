def sum_duration_of_components_in_seconds(components):
   r'''Sum the duration of `components` in seconds.

   ::

      abjad> tuplet = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
      abjad> tempo_spanner = TempoSpanner([tuplet])
      abjad> tempo_indication = tempotools.TempoIndication(Rational(1, 4), 48)
      abjad> tempo_spanner.tempo_indication = tempo_indication
      abjad> f(tuplet)
      \times 2/3 {
         \tempo 4=48
         c'8
         d'8
         e'8
         %% tempo 4=48 ends here
      }
      abjad> componenttools.sum_duration_of_components_in_seconds(tuplet[:])
      Rational(5, 4)

   .. versionchanged:: 1.1.2
      renamed ``durtools.sum_seconds( )`` to
      ``componenttools.sum_duration_of_components_in_seconds( )``.
   '''

   assert isinstance(components, list)
   return sum([component.duration.seconds for component in components])
