from abjad.tools.containertools._report_container_modifications import \
   _report_container_modifications


def report_container_modifications_as_string(container):
   r'''Report `container` modifications as string:

   ::

      abjad> container = Container(macros.scale(12))
      abjad> container.note_head.color = 'red'
      abjad> container.note_head.style = 'harmonic'
      abjad> container.comments.before.append('Container comments')
      abjad> print formattools.wrapper(container)
      {
              \override NoteHead #'style = #'harmonic
              \override NoteHead #'color = #red

              %%% 12 components omitted %%%

              \revert NoteHead #'style
              \revert NoteHead #'color
      }
      abjad> containertools.report_container_modifications_as_string(container)
      "% Container comments\n{\n\t\\override NoteHead #'color = #red\n\t\\override NoteHea
      d #'style = #'harmonic\n\n\t%%% 12 components omitted %%%\n\n\t\\revert NoteHead #'s
      tyle\n\t\\revert NoteHead #'color\n}"
   '''

   return _report_container_modifications(container, output = 'string')
