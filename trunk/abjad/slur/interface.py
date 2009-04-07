from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class _SlurInterface(_Interface, _GrobHandler, _SpannerReceptor):

   def __init__(self, client):
      from abjad.slur.spanner import Slur
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Slur')
      _SpannerReceptor.__init__(self, (Slur, ))
