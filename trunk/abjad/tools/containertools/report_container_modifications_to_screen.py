from abjad.tools.containertools._report_container_modifications import _report_container_modifications


def report_container_modifications_to_screen(container):
   r'''Report `container` modifications to screen:

   ::

      abjad> container = Container("c'8 d'8 e'8 f'8")
      abjad> container.override.note_head.color = 'red'
      abjad> container.override.note_head.style = 'harmonic'

   ::

      abjad> f(container)
      {
         \override NoteHead #'color = #red
         \override NoteHead #'style = #'harmonic
         c'8
         d'8
         e'8
         f'8
         \revert NoteHead #'color
         \revert NoteHead #'style
      }

   ::

      abjad> containertools.report_container_modifications_to_screen(container)
      {
         \override NoteHead #'color = #red
         \override NoteHead #'style = #'harmonic

         %%% 4 components omitted %%%

         \revert NoteHead #'color
         \revert NoteHead #'style
      }

   Return none.
   '''

   _report_container_modifications(container, output = 'screen')
