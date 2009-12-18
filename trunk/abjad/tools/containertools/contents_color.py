def contents_color(container, color):
   '''.. versionadded:: 1.1.2

   Override the color of the following in `container`:
   accidental, beam, dots, note head, rest, stem, tuplet bracket,
   tuplet number. ::

      abjad>
   
   Useful for a type of structural highlighting.
   '''

   container.accidental.color = color
   container.beam.color = color
   container.dots.color = color
   container.note_head.color = color
   container.rest.color = color
   container.stem.color = color
   container.tuplet_bracket.color = color
   container.tuplet_number.color = color

   return container
