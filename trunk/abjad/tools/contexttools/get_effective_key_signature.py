from abjad.tools.contexttools.get_effective_mark import get_effective_mark
from abjad.tools.contexttools.KeySignatureMark import KeySignatureMark


def get_effective_key_signature(component):
   '''.. versionadded:: 1.1.2

   Get effective key signature from `component`.

   .. versionchanged:: 1.1.2
      renamed ``marktools.get_effective_key_signature( )`` to
      ``contexttools.get_effective_key_signature( )``.
   '''

   return get_effective_mark(component, KeySignatureMark)
