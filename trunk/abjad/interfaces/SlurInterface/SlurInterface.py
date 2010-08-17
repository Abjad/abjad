from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface
from abjad.interfaces._SpannerReceptor import _SpannerReceptor


class SlurInterface(_Interface, _FormatContributor, _SpannerReceptor):
   '''Handle LilyPond Slur grob and Abjad Slur spanner.'''

   def __init__(self, client):
      '''Bind to client and LilyPond Slur grob.
         Receive Abjad Slur spanner.'''
      from abjad.tools.spannertools import SlurSpanner
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      _SpannerReceptor.__init__(self, (SlurSpanner, ))
