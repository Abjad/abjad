from abjad.tools.marktools.get_effective_mark import get_effective_mark
from abjad.tools.marktools.ClefMark import ClefMark


def get_effective_clef(component):
   '''.. versionadded:: 1.1.2

   Get effective clef from `component`.
   '''

   return get_effective_mark(component, ClefMark)
