def underscore_delimited_lowercase_to_lowercamelcase(string):
   '''.. versionadded:: 1.1.2

   bass_figure_alignment_positioning ==> bassFigureAlignmentPositioning
   '''

   parts = string.split('_')
   first_part = parts[:1]
   rest_parts = parts[1:]
   rest_parts = [part.title( ) for part in rest_parts]
   all_parts = first_part + rest_parts
   return ''.join(all_parts)
