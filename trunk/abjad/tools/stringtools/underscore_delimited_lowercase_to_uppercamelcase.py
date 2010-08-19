def underscore_delimited_lowercase_to_uppercamelcase(string):
   '''.. versionadded:: 1.1.2

   Change underscore-delimited lowercase `string` to uppercamelcase::

      abjad> string = 'bass_figure_alignment_positioning'
      abjad> stringtools.underscore_delimited_lowercase_to_uppercamelcase(string) 
      'BassFigureAlignmentPositioning'
   '''
   
   parts = string.split('_')
   parts = [part.title( ) for part in parts]
   return ''.join(parts)
