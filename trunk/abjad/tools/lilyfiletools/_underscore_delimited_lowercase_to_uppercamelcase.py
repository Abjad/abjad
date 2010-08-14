def _underscore_delimited_lowercase_to_uppercamelcase(string):
   '''.. versionadded:: 1.1.2

   bass_figure_alignment_positioning ==> BassFigureAlignmentPositioning
   '''
   
   parts = string.split('_')
   parts = [part.title( ) for part in parts]
   return ''.join(parts)
