#from abjad.core import _GrobHandler
#from abjad.interfaces._Interface import _Interface
#
#
#class ScriptInterface(_Interface, _GrobHandler):
#   r'''.. versionadded:: 1.1.2
#
#   Handle LilyPond Script grob. ::
#
#      abjad> t = Staff(macros.scale(4))
#      abjad> t.script.staff_padding = 2
#      abjad> t.script.Y_extent = (-1.5, 1.5)
#      \new Staff \with {
#         \override Script #'Y-extent = #'(-1.5 . 1.5)
#         \override Script #'staff-padding = #2
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
#      _GrobHandler.__init__(self, 'Script')
