from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface
from abjad.interfaces.spanner_receptor.receptor import _SpannerReceptor
from abjad.spanners import TextScriptSpanner


class TextScriptInterface(_Interface, _GrobHandler, _SpannerReceptor):
   r'''.. versionadded:: 1.1.2
   
   Handle LilyPond TextScript grob.

   Receive Abjad TextScriptSpanner. ::

      abjad> t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
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
      '''Bind client and LilyPond TextScript grob.
      Receive Abjad Text spanner.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TextScript')
      _SpannerReceptor.__init__(self, (TextScriptSpanner, ))
