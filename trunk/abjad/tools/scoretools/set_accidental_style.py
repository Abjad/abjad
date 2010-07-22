from abjad.context.context import _Context
from abjad.tools import iterate


def set_accidental_style(expr, accidental_style):
   r'''.. versionadded:: 1.1.2

   Set `accidental_style` for sequential contexts in `expr`. ::

      score = Score(Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(2)) * 2)
      scoretools.set_accidental_style(score, 'forget')
      \new Score <<
              \new Staff {
                      #(set-accidental-style 'forget)
                      c'8
                      d'8
              }
              \new Staff {
                      #(set-accidental-style 'forget)
                      c'8
                      d'8
              }
      >>
   
   .. note:: function looks like a hack but isn't.
      LilyPond uses the dedicated ``#(set-accidental-style 'style)``
      command to set accidental style.
      This means that it is not possible to set accidental style on 
      a top-level context like score with a single override.
   '''

   for context in iterate.naive_forward_in_expr(expr, _Context):
      if not context.parallel:
         context.accidental.style = accidental_style
