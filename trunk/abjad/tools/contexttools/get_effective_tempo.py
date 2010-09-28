from abjad.tools.contexttools.get_effective_mark import get_effective_mark
from abjad.tools.contexttools.TempoMark import TempoMark


def get_effective_tempo(component):
   '''.. versionadded:: 1.1.2

   Get effective tempo from `component`.

   .. versionchanged:: 1.1.2
      renamed ``marktools.get_effective_tempo( )`` to
      ``contexttools.get_effective_tempo( )``.
   '''

   return get_effective_mark(component, TempoMark)
