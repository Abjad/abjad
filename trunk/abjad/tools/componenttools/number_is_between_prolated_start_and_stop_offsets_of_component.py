from fractions import Fraction


def number_is_between_prolated_start_and_stop_offsets_of_component(timepoint, component):
   '''.. versionadded:: 1.1.2

   True when `timepoint` is within the prolated duration of `component`::
   
      abjad> staff = Staff(macros.scale(4))
      abjad> leaf = staff.leaves[0]
      abjad> componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Fraction(1, 16), leaf)
      True
      abjad> componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Fraction(1, 12), leaf)
      True

   Otherwise false::

      abjad> componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Fraction(1, 4), t)
      False

   Return boolean.
   '''

   try:
      timepoint = Fraction(timepoint)
   except TypeError:
      pass

   return component._offset.start <= timepoint < \
      component._offset.stop
