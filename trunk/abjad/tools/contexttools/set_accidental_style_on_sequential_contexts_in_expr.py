from abjad.components._Context import _Context
from abjad.tools import componenttools


def set_accidental_style_on_sequential_contexts_in_expr(expr, accidental_style):
   r'''.. versionadded:: 1.1.2

   Set `accidental_style` for sequential contexts in `expr`. ::

      score = Score(Staff(macros.scale(2)) * 2)
      containertools.set_accidental_style_on_sequential_contexts_in_expr(score, 'forget')
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

   .. versionchanged:: 1.1.2
      renamed ``scoretools.set_accidental_style( )`` to
      ``containertools.set_accidental_style_on_sequential_contexts_in_expr( )``.
   '''

   for context in componenttools.iterate_components_forward_in_expr(expr, _Context):
      if not context.parallel:
         #context.accidental.style = accidental_style
         context.misc.set_accidental_style = accidental_style
