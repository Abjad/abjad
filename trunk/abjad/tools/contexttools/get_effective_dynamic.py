from abjad.tools.contexttools.get_effective_mark import get_effective_mark
from abjad.tools.contexttools.DynamicMark import DynamicMark


def get_effective_dynamic(component):
   '''.. versionadded:: 1.1.2

   Get effective dynamic from `component`.

   .. versionchanged:: 1.1.2
      renamed ``marktools.get_effective_dynamic( )`` to
      ``contexttools.get_effective_dynamic( )``.
   '''

   return get_effective_mark(component, DynamicMark)
