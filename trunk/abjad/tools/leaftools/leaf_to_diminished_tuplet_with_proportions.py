#from abjad.tools.divide._leaf_into_arbitrary_fixed_duration_tuplet import \
#   _leaf_into_arbitrary_fixed_duration_tuplet
from abjad.tools.leaftools._leaf_to_tuplet_with_proportions import \
   _leaf_to_tuplet_with_proportions


def leaf_to_diminished_tuplet_with_proportions(leaf, proportions):
   '''Divide written duration of `leaf` into arbitrary `proportions`.

   Return (diminshed) fixed-duration tuplet. ::

      abjad> note = Note(0, (3, 16))
      abjad> print leaftools.leaf_to_diminished_tuplet_with_proportions(note, [1])
      {@ 1:1 c'8. @}
      abjad> print leaftools.leaf_to_diminished_tuplet_with_proportions(note, [1, 2])
      {@ 1:1 c'16, c'8 @}
      abjad> print leaftools.leaf_to_diminished_tuplet_with_proportions(note, [1, 2, 2])
      {@ 5:3 c'16, c'8, c'8 @}
      abjad> print leaftools.leaf_to_diminished_tuplet_with_proportions(note, [1, 2, 2, 3])
      {@ 4:3 c'32, c'16, c'16, c'16. @}
      abjad> print leaftools.leaf_to_diminished_tuplet_with_proportions(note, [1, 2, 2, 3, 3])
      {@ 11:6 c'32, c'16, c'16, c'16., c'16. @}
      abjad> print leaftools.leaf_to_diminished_tuplet_with_proportions(note, [1, 2, 2, 3, 3, 4])
      {@ 5:4 c'64, c'32, c'32, c'32., c'32., c'16 @}

   .. versionchanged:: 1.1.2
      renamed ``divide.leaf_into_arbitrary_diminution( )`` to
      ``leaftools.leaf_to_diminished_tuplet_with_proportions( )``.
   '''

   #return _leaf_into_arbitrary_fixed_duration_tuplet(l, proportions, 'diminution')
   return _leaf_to_tuplet_with_proportions(leaf, proportions, 'diminution')
