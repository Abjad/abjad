from abjad.tools.pitcharraytools._leaf_iterables_to_pitch_array import \
   _leaf_iterables_to_pitch_array


def make_populated_pitch_array_from_list_of_pitch_lists(leaf_iterables):
   r'''.. versionadded:: 1.1.2

   Return populated pitch array corresponding to `leaf_iterables`. ::

      abjad> score = Score([ ])
      abjad> score.append(Staff(macros.scale(4)))
      abjad> score.append(Staff(macros.scale(2, Fraction(1, 4))))
      abjad> score.append(Staff(tuplettools.FixedDurationTuplet((2, 8), macros.scale(3)) * 2))
      abjad> f(score)
      \new Score <<
              \new Staff {
                      c'8
                      d'8
                      e'8
                      f'8
              }
              \new Staff {
                      c'4
                      d'4
              }
              \new Staff {
                      \times 2/3 {
                              c'8
                              d'8
                              e'8
                      }
                      \times 2/3 {
                              c'8
                              d'8
                              e'8
                      }
              }
      >>

   ::

      abjad> array = pitchtools.make_populated_pitch_array_from_list_of_pitch_lists(score)
      abjad> print array
      [c'     ] [d'     ] [e'     ] [f'     ]
      [c'               ] [d'               ]
      [c'] [d'     ] [e'] [c'] [d'     ] [e']

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.leaf_iterables_to_pitch_array_populated( )`` to
      ``pitchtools.make_populated_pitch_array_from_list_of_pitch_lists( )``.
   '''

   return _leaf_iterables_to_pitch_array(leaf_iterables, populate = True)
