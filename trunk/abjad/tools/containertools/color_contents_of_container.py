def color_contents_of_container(container, color):
   r'''.. versionadded:: 1.1.2

   Set `container` contents to `color`::

      abjad> measure = RigidMeasure((2, 8), macros.scale(2))
      abjad> containertools.color_contents_of_container(measure, 'red')
      {
              \override Accidental #'color = #red
              \override Beam #'color = #red
              \override Dots #'color = #red
              \override NoteHead #'color = #red
              \override Rest #'color = #red
              \override Stem #'color = #red
              \override TupletBracket #'color = #red
              \override TupletNumber #'color = #red
              \time 2/8
              c'8
              d'8
              \revert Accidental #'color
              \revert Beam #'color
              \revert Dots #'color
              \revert NoteHead #'color
              \revert Rest #'color
              \revert Stem #'color
              \revert TupletBracket #'color
              \revert TupletNumber #'color
      }
   
   Use to highlight structure.

   .. versionchanged:: 1.1.2
      renamed ``containertools.contents_color( )`` to
      ``containertools.color_contents_of_container( )``.
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
