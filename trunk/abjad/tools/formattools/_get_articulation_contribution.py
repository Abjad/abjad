def _get_articulation_contribution(component):
   '''.. versionadded:: 1.1.2
   '''
   from abjad.tools import marktools

   result = [ ]
   articulations = marktools.get_articulations_attached_to_component(component)
   for articulation in articulations:
      result.append(articulation.format)
   result.sort( )
   return result
