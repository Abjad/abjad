from abjad.tools.marktools.get_effective_mark import get_effective_mark
from abjad.tools.marktools.KeySignatureMark import KeySignatureMark


def get_effective_key_signature(component):
   '''.. versionadded:: 1.1.2

   Get effective key signature from `component`.
   '''

   return get_effective_mark(component, KeySignatureMark)
