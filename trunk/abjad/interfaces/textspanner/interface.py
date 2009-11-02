from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface
from abjad.spanners.spanner.receptor import _SpannerReceptor
#from abjad.spanners.text import Text


class TextSpannerInterface(_Interface, _GrobHandler, _SpannerReceptor):
   r'''Handle LilyPond TextSpanner grob.

   .. todo:: implement Abjad TextSpannerSpanner.

   ::

      abjad> t = Staff(construct.scale(4))
      abjad> t.text_spanner.staff_padding = 6
      abjad> Text(t[:])
      \new Staff \with {
         \override TextSpanner #'staff-padding = #6
      } {
         c'8 \startTextSpan
         d'8
         e'8
         f'8 \stopTextSpan
      }
   '''

   def __init__(self, client):
      '''Bind client and LilyPond TextScript grob.
      Receive Abjad Text spanner.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TextSpanner')
      #_SpannerReceptor.__init__(self, (Text, ))
