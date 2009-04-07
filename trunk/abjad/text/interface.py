from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class _TextInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond TextScript grob.
      Receive Abjad Text spanner.'''

   def __init__(self, client):
      '''Bind client and LilyPond TextScript grob.
         Receive Abjad Text spanner.'''
      from abjad.text.spanner import Text
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TextScript')
      _SpannerReceptor.__init__(self, (Text, ))
