def sum_seconds(components):
   r'''Sum of the duration of each component in `components`, in seconds.

   ::

      abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))
      abjad> tempo = Tempo([t])
      abjad> tempo.indication = TempoIndication(Rational(1, 4), 48)
      abjad> print t.format

      \times 2/3 {
         \tempo 4=48
         c'8
         d'8
         e'8
         %% tempo 4=48 ends here
      }

      abjad> durtools.sum_seconds(t[:])
      Rational(5, 4)
   '''

   assert isinstance(components, list)
   return sum([component.duration.seconds for component in components])
