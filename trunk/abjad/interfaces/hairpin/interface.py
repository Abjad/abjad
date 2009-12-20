from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface


class HairpinInterface(_Interface, _GrobHandler):
   r'''.. versionadded:: 1.1.2

   Handle LilyPond Hairpin grob. ::

      abjad> t = Staff(construct.scale(4))
      abjad> t.hairpin.staff_padding = 2
      abjad> t.hairpin.Y_extent = (-1.5, 1.5)
      \new Staff \with {
         \override Hairpin #'Y-extent = #'(-1.5 . 1.5)
         \override Hairpin #'staff-padding = #2
      } {
         c'8
         d'8
         e'8
         f'8
      }
   '''

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Hairpin')
