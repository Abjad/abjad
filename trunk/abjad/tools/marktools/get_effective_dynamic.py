from abjad.tools.marktools.get_effective_mark import get_effective_mark
from abjad.tools.marktools.DynamicMark import DynamicMark


def get_effective_dynamic(component):
   '''.. versionadded:: 1.1.2

   Get effective dynamic from `component`.
   '''

   return get_effective_mark(component, DynamicMark)
