from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces._Interface import _Interface
from abjad.spanners import Glissando
from abjad.interfaces._SpannerReceptor import _SpannerReceptor


class GlissandoInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond ``Glissando`` grob.
   Receive Abjad ``Glissando`` spanner.'''

   def __init__(self, _client):
      '''Bind to client. Handle LilyPond ``Glissando`` grob.
      Receive Ajbad ``Glissando`` spanner.'''
      _Interface.__init__(self, _client)
      _GrobHandler.__init__(self, 'Glissando')
      _SpannerReceptor.__init__(self, (Glissando, ))
