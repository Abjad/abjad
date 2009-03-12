from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class _TextInterface(_Interface, _GrobHandler, _SpannerReceptor):

   def __init__(self, client):
      from abjad.text.spanner import Text
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TextScript')
      #_SpannerReceptor.__init__(self, ['Text'])
      _SpannerReceptor.__init__(self, (Text, ))
