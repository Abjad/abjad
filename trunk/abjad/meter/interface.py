from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.helpers.in_terms_of import _in_terms_of
from abjad.meter.meter import Meter
import types


class _MeterInterface(_Interface, _GrobHandler):
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TimeSignature')
      self._forced = None
      self.suppress = False

   ### PRIVATE ATTRIBUTES ###

   ### NOTE: _MeterInterface formats only _opening and not _before.
   ###       The reason for this is that LilyPond meter indications
   ###       of the form \time 5/16 need print only once,
   ###       from the measure, rather than printing twice, once from
   ###       the measure and once from the first leaf in measure.
   ###       There's a larger question here about which component(s)
   ###       are to be responsible for printing meter indications
   ###       at format-time.

   @property
   def _opening(self):
      result = [ ]
      result.extend(_GrobHandler._before.fget(self))
      effective = self.effective
      #if not effective.suppress:
      if not self.suppress and not effective.suppress:
         if self._client.kind('DynamicMeasure'):
            result.append(self.effective.format)
         else:
            if self.forced or self.change:
               result.append(self.effective.format)
      return result

   ### PUBLIC ATTRIBUTES ###

   @property
   def change(self):
      client = self._client
      return bool(client.prev and \
         client.prev.meter.effective != self.effective)

   ### TODO - the explicit check for DynamicMeasure seems like
   ###        a (small) hack; is there a better implementation?

   @property
   def effective(self):
      client = self._client
      if client.kind('DynamicMeasure'):
         if client.denominator:
            return Meter(
               _in_terms_of(client.duration.contents, client.denominator))
         else:
            return Meter(client.duration.contents)
      cur = self._client
      while cur is not None:
         if cur.meter._forced:
            return cur.meter._forced
         else:
            cur = cur.prev
      for x in self._client.parentage.parentage[1:]:
         if hasattr(x, 'meter') and x.meter._forced:
            return x.meter._forced
      return Meter(4, 4)

   @apply
   def forced( ):
      def fget(self):
         return self._forced
      def fset(self, arg):
         if arg is None:
            self._forced = None
         elif isinstance(arg, tuple):
            meter = Meter(*arg)
            self._forced = meter
         elif isinstance(arg, Meter):
            self._forced = arg
         else:
            raise ValueError('unknown meter specification.')
      return property(**locals( ))

   @apply
   def suppress( ):
      def fget(self):
         return self._suppress
      def fset(self, arg):
         assert isinstance(arg, (bool, types.NoneType))
         self._suppress = arg
      return property(**locals( ))
