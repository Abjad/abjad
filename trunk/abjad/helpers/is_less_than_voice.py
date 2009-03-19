from abjad.component.component import _Component
from abjad.context.context import _Context


def _is_less_than_voice(expr):
   '''True when expr is an Abjad component that
      can be *contained* in an Abjad voice.
      Leaves, tuplets, measures are all examples.
      Otherwise False.'''

   return isinstance(expr, _Component) and not isinstance(expr, _Context)
