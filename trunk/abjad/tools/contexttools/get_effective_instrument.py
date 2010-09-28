from abjad.tools.contexttools.get_effective_mark import get_effective_mark
from abjad.tools.contexttools.InstrumentMark import InstrumentMark


def get_effective_instrument(component):
   '''.. versionadded:: 1.1.2

   Get effective instrument from `component`.

   .. versionchanged:: 1.1.2
      renamed ``marktools.get_effective_instrument( )`` to
      ``contexttools.get_effective_instrument( )``.
   '''

   return get_effective_mark(component, InstrumentMark)
