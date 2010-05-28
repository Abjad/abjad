from abjad.tools import check


def get_duration_preprolated(components):
   r'''Sum the preprolated duration of each component in `components`. ::

      abjad> tuplet = FixedDurationTuplet((2, 8), construct.scale(3))
      abjad> componenttools.get_duration_preprolated(tuplet[:])
      Rational(3, 8)

   Return zero on empty iterable. ::

      abjad> componenttools.get_duration_preprolated([ ])
      Rational(0)

   Raise contiguity error on nonparent-contiguous `components`. ::

      abjad> t = Voice(FixedDurationTuplet((2, 8), construct.run(3)) * 2)
      abjad> pitchtools.diatonicize(t)
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
      abjad> componenttools.get_duration_preprolated(t.leaves)
      ContiguityError
   '''

   ## check input
   check.assert_components(components, contiguity = 'strict', share = 'parent')

   ## sum preprolated durations
   result = sum([component.duration.preprolated for component in components])

   ## return sum
   return result
