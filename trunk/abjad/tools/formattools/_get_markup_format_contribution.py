def _get_markup_format_contribution(component):
   '''.. versionadded:: 1.1.2
   '''
   from abjad.tools import markuptools

   result = [ ]
   markups = markuptools.get_markup_attached_to_component(component)
   for markup in markups:
      result.append(markup.format)
   result.sort( )
   return result
