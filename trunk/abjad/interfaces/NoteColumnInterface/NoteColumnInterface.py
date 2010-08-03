from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces._Interface import _Interface


class NoteColumnInterface(_Interface, _GrobHandler):
   r'''.. versionadded:: 1.1.1.

   Handle the LilyPond NoteColumn grob. ::

      abjad> t = Staff(macros.scale(4))
      abjad> t.note_column.ignore_collision = True

   ::

      abjad> print t.format
      \new Staff \with {
         \override NoteColumn #'ignore-collision = ##t
      } {
         c'8
         d'8
         e'8
         f'8
      }
   '''

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'NoteColumn')
