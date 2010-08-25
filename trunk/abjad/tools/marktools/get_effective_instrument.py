from abjad.tools.marktools.get_effective_mark import get_effective_mark
from abjad.tools.marktools.InstrumentMark import InstrumentMark


def get_effective_instrument(component):
   '''.. versionadded:: 1.1.2

   Get effective instrument from `component`.
   '''

   return get_effective_mark(component, InstrumentMark)
