from abjad.core import _Abjad
from abjad.core import _Immutable


class SchemeColor(_Abjad, _Immutable):
   '''Wrapper for names of X-11 colors known to LilyPond.

   ::

      abjad> t = Note(0, (1, 4))
      abjad> t.override.note_head.color = schemetools.SchemeColor('ForestGreen')
      abjad> print t.format
      \once \override NoteHead #'color = #(x11-color 'ForestGreen)
      c'4
   '''

   def __init__(self, name):
      object.__setattr__(self, 'name', name)

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def format(self):
      '''LilyPond embedded Scheme call for color.'''
      return "#(x11-color '%s)" % self.name
