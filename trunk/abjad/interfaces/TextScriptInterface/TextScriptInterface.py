from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface
from abjad.interfaces._SpannerReceptor import _SpannerReceptor


class TextScriptInterface(_Interface, _FormatContributor, _SpannerReceptor):
   r'''.. versionadded:: 1.1.2
   
   Handle LilyPond TextScript grob.

   Receive Abjad TextScriptSpanner. ::

      abjad> t = Staff(macros.scale(4))
      abjad> t[0].markup.up.append(r'\italic { Lento }')
      abjad> t.text_script.staff_padding = 6
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
      from abjad.tools.spannertools import TextScriptSpanner
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      _SpannerReceptor.__init__(self, (TextScriptSpanner, ))
