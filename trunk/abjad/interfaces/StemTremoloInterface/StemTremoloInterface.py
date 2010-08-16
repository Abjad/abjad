#from abjad.core import _GrobHandler
#from abjad.interfaces._Interface import _Interface
#
#
#class StemTremoloInterface(_Interface, _GrobHandler):
#   r'''.. versionadded:: 1.1.2
#
#   Handle LilyPond StemTremolo grob. ::
#
#      abjad> t = Staff(macros.scale(4))
#      abjad> t.stem_tremolo.staff_padding = 2
#      abjad> t.stem_tremolo.Y_extent = (-1.5, 1.5)
#      \new Staff \with {
#         \override StemTremolo #'Y-extent = #'(-1.5 . 1.5)
#         \override StemTremolo #'staff-padding = #2
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
#      _GrobHandler.__init__(self, 'StemTremolo')
