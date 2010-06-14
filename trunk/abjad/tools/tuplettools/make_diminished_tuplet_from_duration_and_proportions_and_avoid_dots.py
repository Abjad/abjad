#from abjad.tools.divide._duration_into_arbitrary_fixed_duration_tuplet_undotted import \
#   _duration_into_arbitrary_fixed_duration_tuplet_undotted
from abjad.tools.tuplettools._make_tuplet_from_duration_with_proportions_and_avoid_dots \
   import _make_tuplet_from_duration_with_proportions_and_avoid_dots

def make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(duration, proportions):
   r'''.. versionadded:: 1.1.2

   Divide `duration` into fixed-duration tuplet 
   according to arbitrary integer `proportions`.  

   Reduce the values in `proportions` relative to each other.

   Return non-trivial tuplets as diminutions.

   Where ``proportions[i] == 1`` for all ``i <= len(proportions) - 1``, 
   return tupletted notes strictly without dots. ::

      abjad> duration = Rational(3, 16)
      abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(duration, [1])
      {@ 4:3 c'4 @}
      abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(duration, [1, 1])
      {@ 4:3 c'8, c'8 @}
      abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(duration, [1, 1, 1])
      {@ 1:1 c'16, c'16, c'16 @}
      abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(duration, [1, 1, 1, 1])
      {@ 4:3 c'16, c'16, c'16, c'16 @}
      abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(duration, [1, 1, 1, 1, 1])
      {@ 5:3 c'16, c'16, c'16, c'16, c'16 @}

   Where ``proportions[i] != 1`` for some ``i <= len(proportions) - 1``, 
   allow tupletted notes to return with dots. ::

      abjad> duration = Rational(3, 16)
      abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(duration, [1])
      {@ 4:3 c'4 @}
      abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(duration, [1, 2])
      {@ 1:1 c'16, c'8 @}
      abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(duration, [1, 2, 2])
      {@ 5:3 c'16, c'8, c'8 @}
      abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(duration, [1, 2, 2, 3])
      {@ 4:3 c'32, c'16, c'16, c'16. @}
      abjad> print tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots(duration, [1, 2, 2, 3, 3])
      {@ 11:6 c'32, c'16, c'16, c'16., c'16. @}

   .. versionchanged:: 1.1.2
      renamed ``divide.duration_into_arbitrary_diminution_undotted( )`` to
      ``tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots( )``.
   '''

   #return _duration_into_arbitrary_fixed_duration_tuplet_undotted(
   #   duration, proportions, 'diminution')
   return _make_tuplet_from_duration_with_proportions_and_avoid_dots(
      duration, proportions, 'diminution')
