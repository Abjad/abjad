#from abjad.core import _FormatContributor
#from abjad.interfaces._Interface import _Interface
#
#
#class HairpinInterface(_Interface, _FormatContributor):
#   r'''.. versionadded:: 1.1.2
#
#   Handle LilyPond Hairpin grob. ::
#
#      abjad> t = Staff(macros.scale(4))
#      abjad> t.hairpin.staff_padding = 2
#      abjad> t.hairpin.Y_extent = (-1.5, 1.5)
#      \new Staff \with {
#         \override Hairpin #'Y-extent = #'(-1.5 . 1.5)
#         \override Hairpin #'staff-padding = #2
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
#      _FormatContributor.__init__(self)
