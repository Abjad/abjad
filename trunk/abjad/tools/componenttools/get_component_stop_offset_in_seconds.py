def get_component_stop_offset_in_seconds(component):
   r'''.. versionadded:: 1.1.1

   Get `component` stop offset in seconds::

      abjad> staff = Staff(macros.scale(4))
      abjad> score = Score([staff])
      abjad> contexttools.TempoMark(Fraction(1, 4), 52)(score)
      abjad> f(score)
      \new Score <<
         \new Staff {
            \tempo 4=52
            c'8
            d'8
            e'8
            f'8
         }
      >>

   ::

      abjad> componenttools.get_component_stop_offset_in_seconds(score.leaves[1])
      Fraction(15, 13)

   Return positive fraction.
   '''

   return component._offset.stop_in_seconds
