from abjad.container.container import Container
from abjad.context.context import _Context


def _is_voice_guarantor(expr):
   '''True when expr is an Abjad context or parallel container,
      otherwise False.'''

   return isinstance(expr, _Context) or \
      (isinstance(expr, Container) and getattr(expr, 'parallel', False))
