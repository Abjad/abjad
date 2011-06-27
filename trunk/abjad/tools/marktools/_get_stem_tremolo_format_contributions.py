def _get_stem_tremolo_format_contributions(component):
   '''.. versionadded:: 1.1.2
   '''
   from abjad.tools import marktools

   result = [ ]
   stem_tremolos = marktools.get_stem_tremolos_attached_to_component(component)
   for stem_tremolo in stem_tremolos:
      result.append(stem_tremolo.format)
   result.sort( )
   return result
