from abjad.tools.divide._leaf_into_arbitrary_fixed_duration_tuplet import \
   _leaf_into_arbitrary_fixed_duration_tuplet


def leaf_into_arbitrary_diminution(l, divisions):
   '''Divide written duration of `l` into arbitrary `divisions`.

   Return (diminshed) fixed-duration tuplet. ::

      abjad> note = Note(0, (3, 16))
      abjad> print divide.leaf_into_arbitrary_diminution(note, [1])
      {@ 1:1 c'8. @}
      abjad> print divide.leaf_into_arbitrary_diminution(note, [1, 2])
      {@ 1:1 c'16, c'8 @}
      abjad> print divide.leaf_into_arbitrary_diminution(note, [1, 2, 2])
      {@ 5:3 c'16, c'8, c'8 @}
      abjad> print divide.leaf_into_arbitrary_diminution(note, [1, 2, 2, 3])
      {@ 4:3 c'32, c'16, c'16, c'16. @}
      abjad> print divide.leaf_into_arbitrary_diminution(note, [1, 2, 2, 3, 3])
      {@ 11:6 c'32, c'16, c'16, c'16., c'16. @}
      abjad> print divide.leaf_into_arbitrary_diminution(note, [1, 2, 2, 3, 3, 4])
      {@ 5:4 c'64, c'32, c'32, c'32., c'32., c'16 @}
   '''

   return _leaf_into_arbitrary_fixed_duration_tuplet(
      l, divisions, 'diminution')
