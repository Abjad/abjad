#from abjad.core import _GrobHandler
#from abjad.interfaces._Interface import _Interface
#
#
#class DynamicTextInterface(_Interface, _GrobHandler):
#   r'''.. versionadded:: 1.1.2
#
#   Handle LilyPond DynamicText grob. ::
#
#      abjad> t = Staff(macros.scale(4))
#      abjad> t.dynamic_line_spanner.staff_padding = 2
#      abjad> t.dynamic_line_spanner.Y_extent = (-1.5, 1.5)
#      \new Staff \with {
#         \override DynamicText #'Y-extent = #'(-1.5 . 1.5)
#         \override DynamicText #'staff-padding = #2
#      } {
#         c'8
#         d'8
#         e'8
#         f'8
#      }
#   '''
#
#   def __init__(self, client):
#      _Interface.__init__(self, client)
#      _GrobHandler.__init__(self, 'DynamicText')
