from abjad.core import _GrobHandler
from abjad.interfaces._Interface import _Interface
from abjad.interfaces._SpannerReceptor import _SpannerReceptor
from abjad.spanners import TextSpanner


class TextSpannerInterface(_Interface, _GrobHandler, _SpannerReceptor):
   r'''.. versionadded:: 1.1.2

   Handle LilyPond TextSpanner grob.

   Receive Abjad TextSpanner. ::

      abjad> t = Staff(macros.scale(4))
      abjad> t.text_spanner.staff_padding = 6
      abjad> TextSpanner(t[:])
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
      _SpannerReceptor.__init__(self, (TextSpanner, ))
