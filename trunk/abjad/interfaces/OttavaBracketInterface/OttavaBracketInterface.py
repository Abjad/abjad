from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces._Interface import _Interface


class OttavaBracketInterface(_Interface, _GrobHandler):
   r'''.. versionadded:: 1.1.2

   Handle LilyPond OttavaBracket grob. ::

      abjad> t = Staff(macros.scale(4))
      abjad> t.ottava_bracket.staff_padding = 2
      abjad> t.ottava_bracket.Y_extent = (-1.5, 1.5)
      \new Staff \with {
         \override OttavaBracket #'Y-extent = #'(-1.5 . 1.5)
         \override OttavaBracket #'staff-padding = #2
      } {
         c'8
         d'8
         e'8
         f'8
      }
   '''

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'OttavaBracket')
