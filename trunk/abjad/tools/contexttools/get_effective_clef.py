from abjad.tools.contexttools.get_effective_mark import get_effective_mark
from abjad.tools.contexttools.ClefMark import ClefMark


def get_effective_clef(component):
   '''.. versionadded:: 1.1.2

   Get effective clef from `component`.

   .. versionchanged:: 1.1.2
      renamed ``marktools.get_effective_clef( )`` to
      ``contexttools.get_effective_clef( )``.
   '''

   return get_effective_mark(component, ClefMark)
