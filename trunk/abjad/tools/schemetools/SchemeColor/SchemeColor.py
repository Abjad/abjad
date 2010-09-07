from abjad.core import _StrictComparator
from abjad.core import _Immutable


class SchemeColor(_StrictComparator, _Immutable):
   '''Wrapper for names of X-11 colors known to LilyPond.

   ::

      abjad> t = Note(0, (1, 4))
      abjad> t.override.note_head.color = schemetools.SchemeColor('ForestGreen')
      abjad> print t.format
      \once \override NoteHead #'color = #(x11-color 'ForestGreen)
      c'4
   '''

   def __new__(klass, name):
      self = object.__new__(klass)
      object.__setattr__(self, 'name', name)
      return self

   def __getnewargs__(self):
      return (self.name,)

#   def __init__(self, name):
#      object.__setattr__(self, 'name', name)

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def format(self):
      '''LilyPond embedded Scheme call for color.'''
      return "#(x11-color '%s)" % self.name
