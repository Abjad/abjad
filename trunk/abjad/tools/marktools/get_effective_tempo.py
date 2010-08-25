from abjad.tools.marktools.get_effective_mark import get_effective_mark
from abjad.tools.marktools.TempoMark import TempoMark


def get_effective_tempo(component):
   '''.. versionadded:: 1.1.2

   Get effective tempo from `component`.
   '''

   return get_effective_mark(component, TempoMark)
