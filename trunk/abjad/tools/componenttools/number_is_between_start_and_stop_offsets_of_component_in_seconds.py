from fractions import Fraction


def number_is_between_start_and_stop_offsets_of_component_in_seconds(timepoint, component):
   '''.. versionadded:: 1.1.2

   True when `timepoint` is within the duration of `component` in seconds::
   
      abjad> staff = Staff(macros.scale(4))
      abjad> contexttools.TempoMark(Fraction(1, 2), 60, target_context = Staff)(staff)
      TempoMark(2, 60)(Staff{4})

   ::
      
      abjad> leaf = staff.leaves[0]
      abjad> componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds(0.1, leaf)
      True
      abjad> componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds(0.333, leaf) # doctest: +SKIP
      True

   Otherwise false::

      abjad> componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds(0.5, staff) # doctest: +SKIP
      False

   Return boolean.
   '''

   try:
      timepoint = Fraction(timepoint)
   except TypeError:
      pass

   return component._offset.start_in_seconds <= timepoint < \
      component._offset.stop_in_seconds
