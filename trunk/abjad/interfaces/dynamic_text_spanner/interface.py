from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface
from abjad.spanners import TextSpanner


class DynamicTextSpannerInterface(_Interface, _GrobHandler):
   r'''.. versionadded:: 1.1.2

   Handle LilyPond DynamicTextSpanner grob. ::

      abjad> t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> t.dynamic_line_spanner.staff_padding = 2
      abjad> t.dynamic_line_spanner.Y_extent = (-1.5, 1.5)
      \new Staff \with {
         \override DynamicTextSpanner #'Y-extent = #'(-1.5 . 1.5)
         \override DynamicTextSpanner #'staff-padding = #2
      } {
         c'8
         d'8
         e'8
         f'8
      }
   '''

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'DynamicTextSpanner')
