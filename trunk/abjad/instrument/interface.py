from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class _InstrumentInterface(_Interface, _SpannerReceptor):
   '''Receives Abjad Instrument spanner.'''

   def __init__(self, client):
      from abjad.instrument.spanner import Instrument
      _Interface.__init__(self, client)
      _SpannerReceptor.__init__(self, (Instrument, ))
