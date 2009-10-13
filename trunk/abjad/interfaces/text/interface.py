from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor
from abjad.spanners.text import Text


class TextInterface(_Interface, _GrobHandler, _SpannerReceptor):
   r'''Handle LilyPond TextScript grob.
   Receive Abjad Text spanner.

   The `Abjad` :class:`~abjad.text.interface.TextInterface` handles
   the `LilyPond` `TextScript` grob.

   ::

      abjad> t = Staff(construct.scale(4))
      abjad> t[0].markup.up.append(r'\italic { Lento }')
      abjad> t.text.staff_padding = 6
      \new Staff \with {
         \override TextScript #'staff-padding = #6
      } {
         c'8 ^ \markup { \italic { Lento } }
         d'8
         e'8
         f'8
      }
   '''

   def __init__(self, client):
      '''Bind client and LilyPond TextScript grob.
         Receive Abjad Text spanner.'''
      #from abjad.text import Text
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TextScript')
      _SpannerReceptor.__init__(self, (Text, ))
