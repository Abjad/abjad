from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface
from abjad.spanners.glissando.spanner import Glissando
from abjad.interfaces.spanner_receptor.receptor import _SpannerReceptor


class GlissandoInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond ``Glissando`` grob.
      Receive Abjad ``Glissando`` spanner.'''

   def __init__(self, _client):
      '''Bind to client. Handle LilyPond ``Glissando`` grob.
      Receive Ajbad ``Glissando`` spanner.'''

      #from abjad.glissando.spanner import Glissando
      _Interface.__init__(self, _client)
      _GrobHandler.__init__(self, 'Glissando')
      _SpannerReceptor.__init__(self, (Glissando, ))
