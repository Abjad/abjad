from abjad.Rational import Rational


def number_is_between_prolated_start_and_stop_offsets_of_component(timepoint, component):
   '''True when `timepoint` is within the prolated 
   duration of `component`. ::
   
      abjad> staff = Staff(macros.scale(4))
      abjad> leaf = staff.leaves[0]
      abjad> componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Rational(1, 16), leaf)
      True
      abjad> componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Rational(1, 12), leaf)
      True

   Otherwise false. ::

      abjad> componenttools.number_is_between_prolated_start_and_stop_offsets_of_component(Rational(1, 4), t)
      False

   .. versionchanged:: 1.1.2
      renamed ``durtools.within_prolated( )`` to
      ``componenttools.number_is_between_prolated_start_and_stop_offsets_of_component( )``.
   '''

   try:
      timepoint = Rational(timepoint)
   except TypeError:
      pass

   return component.offset.prolated.start <= timepoint < \
      component.offset.prolated.stop
