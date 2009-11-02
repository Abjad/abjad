from abjad.tools.divide._duration_into_arbitrary_fixed_duration_tuplet import \
   _duration_into_arbitrary_fixed_duration_tuplet


def duration_into_arbitrary_diminution(duration, divisions):
   r'''Divide `duration` into arbitrary `divisions`.

   Return (diminshed) fixed-duration tuplet. ::

      abjad> duration = Rational(3, 16)
      abjad> print divide.duration_into_arbitrary_diminution(duration, [1])
      {@ 1:1 c'8. @}
      abjad> print divide.duration_into_arbitrary_diminution(duration, [1, 2])
      {@ 1:1 c'16, c'8 @}
      abjad> print divide.duration_into_arbitrary_diminution(duration, [1, 2, 2])
      {@ 5:3 c'16, c'8, c'8 @}
      abjad> print divide.duration_into_arbitrary_diminution(duration, [1, 2, 2, 3])
      {@ 4:3 c'32, c'16, c'16, c'16. @}
      abjad> print divide.duration_into_arbitrary_diminution(duration, [1, 2, 2, 3, 3])
      {@ 11:6 c'32, c'16, c'16, c'16., c'16. @}
      abjad> print divide.duration_into_arbitrary_diminution(duration, [1, 2, 2, 3, 3, 4])
      {@ 5:4 c'64, c'32, c'32, c'32., c'32., c'16 @}
   '''

   return _duration_into_arbitrary_fixed_duration_tuplet(
      duration, divisions, 'diminution')
