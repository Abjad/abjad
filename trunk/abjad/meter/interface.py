from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.helpers.in_terms_of import _in_terms_of
from abjad.meter.meter import Meter


class _MeterInterface(_Interface, _GrobHandler):
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TimeSignature')
      self._forced = None

   ### PRIVATE ATTRIBUTES ###

   @property
   def _before(self):
      result = [ ]
      result.extend(_GrobHandler._before.fget(self))
      if self._client.kind('DynamicMeasure'):
         result.append(self.effective.format)
      else:
         if self.forced or self.change:
            result.append(self.effective.format)
      return result

   ### NOTE: this is kinda kinky:
   ###       reusing _before as _opening;

   @property
   def _opening(self):
      return self._before

   ### PUBLIC ATTRIBUTES ###

   @property
   def change(self):
      return bool(self._client.prev and \
         self._client.prev.meter.pair != self.pair)

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
      #for x in self._client._parentage._parentage:
      #for x in self._client._parentage._iparentage[1:]:
      #for x in self._client._parentage._parentage[1:]:
      #for x in self._client.parentage._parentage[1:]:
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

   @property
   def pair(self):
      return self.effective.pair
