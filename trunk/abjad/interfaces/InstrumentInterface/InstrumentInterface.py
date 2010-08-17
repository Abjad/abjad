from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface
from abjad.interfaces._SpannerReceptor import _SpannerReceptor
from abjad.marks import Markup


class InstrumentInterface(_Interface, _FormatContributor, _SpannerReceptor):
   r'''Receive Abjad InstrumentSpanner.
   '''

   def __init__(self, client):
      from abjad.tools.spannertools import InstrumentSpanner
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      _SpannerReceptor.__init__(self, (InstrumentSpanner, ))
      self._short_name = None
      self._name = None
