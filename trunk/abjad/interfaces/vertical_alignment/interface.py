from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface


class VerticalAlignmentInterface(_Interface, _GrobHandler):
   r'''.. versionadded:: 1.1.2

   Handle LilyPond VerticalAlignment grob. ::

      abjad> t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> t.vertical_alignment.staff_padding = 2
      abjad> t.vertical_alignment.Y_extent = (-1.5, 1.5)
      \new Staff \with {
         \override VerticalAlignment #'Y-extent = #'(-1.5 . 1.5)
         \override VerticalAlignment #'staff-padding = #2
      } {
         c'8
         d'8
         e'8
         f'8
      }
   '''

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'VerticalAlignment')
