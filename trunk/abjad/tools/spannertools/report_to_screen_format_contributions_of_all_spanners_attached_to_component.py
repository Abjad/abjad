from abjad.tools.spannertools.report_format_contributions_of_all_spanners_attached_to_component_as_string import report_format_contributions_of_all_spanners_attached_to_component_as_string


def report_to_screen_format_contributions_of_all_spanners_attached_to_component(
   component, klass = None):
   r'''.. versionadded:: 1.1.1

   Report to screen format contributions of all spanners attached to `component`::

      abjad> staff = Staff(macros.scale(4))
      abjad> beam = spannertools.BeamSpanner(staff.leaves)
      abjad> slur = spannertools.SlurSpanner(staff.leaves)
      abjad> trill = spannertools.TrillSpanner(staff)
      abjad> f(staff)
      \new Staff {
         c'8 [ ( \startTrillSpan
         d'8
         e'8
         f'8 ] ) \stopTrillSpan
      }
      
   ::
      
      abjad> spannertools.report_format_contributions_of_all_spanners_attached_to_component_to_screen(staff[0])
      BeamSpanner
         _right
            [
      SlurSpanner
         _right
            (
   '''

   report = report_format_contributions_of_all_spanners_attached_to_component_as_string(
      component, klass)
   
   print report
