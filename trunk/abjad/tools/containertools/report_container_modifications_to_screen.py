from abjad.tools.containertools._report_container_modifications import \
   _report_container_modifications


def report_container_modifications_to_screen(container):
   r'''Report `container` modifications to screen:

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
   '''

   _report_container_modifications(container, output = 'screen')
