def get_beam_spanner(component):
   '''.. versionadded:: 1.1.2

   Get the only beam spanner attached to `component`.

   Raise missing spanner error when no beam spanner attached to `component`.

   Raise extra spanner error when more than one beam spanner attached to `component`.
   '''
   from abjad.tools import spannertools

   return spannertools.get_the_only_spanner_attached_to_component(
      component, spannertools.BeamSpanner)
