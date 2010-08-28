from abjad.tools.marktools.get_effective_mark import get_effective_mark
from abjad.tools.marktools.TimeSignatureMark import TimeSignatureMark


def get_effective_time_signature(component):
   '''.. versionadded:: 1.1.2

   Get effective time signature from `component`.
   '''

   explicit_meter = getattr(component, '_explicit_meter', None)
   if explicit_meter is not None:
      return explicit_meter
   else:
      return get_effective_mark(component, TimeSignatureMark)
