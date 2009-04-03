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

   ## PRIVATE ATTRIBUTES ##

   @property
   def _selfCanContribute(self):
      r'''True when self is able to contribute LilyPond \time.'''
      from abjad.measure.dynamic.measure import DynamicMeasure
      if not self.suppress:
         if isinstance(self._client, DynamicMeasure):
            return True
         elif self.forced or self.change:
            return True
      return False

   @property
   def _selfShouldContribute(self):
      r'''True when self should contribute LilyPond \time.'''
      return self._selfCanContribute and not self._parentCanContribute

   @property
   def _parentCanContribute(self):
      r'''True when any parent, other than self, can contribute LP \time.'''
      parentage = self._client.parentage.parentage[1:]
      for parent in parentage:
         try:
            if parent.meter._selfCanContribute:
               return True
         except AttributeError:
            pass
      return False

   ## PUBLIC ATTRIBUTES ##

   ## TODO: Deprecate _MeterInterface.opening in favor of .before ##
   ## TODO: Use .opening in only VERY special cases ##

   @property
   def before(self):
      '''List of formatting contributions at _before location.'''
      return self._opening

   @property
   def opening(self):
      '''List of formatting contributions at _opening location.'''
      result = [ ]
      result.extend(_GrobHandler.before.fget(self))
      if self._selfShouldContribute:
         result.append(self.effective.format)
      return result

   @property
   def change(self):
      '''True if meter of client differs from 
         meter of component previous to client.'''
      client = self._client
      #return bool(client.prev and \
      #   client.prev.meter.effective != self.effective)
      ## should there be explicit measure-navigation in navigator?
      return bool(client._navigator._prevBead and \
         client._navigator._prevBead.meter.effective != self.effective)

   ## TODO - the explicit check for DynamicMeasure seems like
   ##        a (small) hack; is there a better implementation?

   @property
   def effective(self):
      '''Return reference to meter effectively governing client.'''
      from abjad.measure.dynamic.measure import DynamicMeasure
      client = self._client
      if isinstance(client, DynamicMeasure):
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
            #cur = cur.prev
            ## should there be explicit measure-navigation in navigator?
            cur = cur._navigator._prevBead
      for x in self._client.parentage.parentage[1:]:
         if hasattr(x, 'meter') and x.meter._forced:
            return x.meter._forced
      return Meter(4, 4)

   @apply
   def forced( ):
      '''Read / write attribute to set meter explicitly.'''
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
      r'''Read / write attribute to suppress contribution
         of LilyPond \time indication at format-time.'''
      def fget(self):
         return self._suppress
      def fset(self, arg):
         assert isinstance(arg, (bool, types.NoneType))
         self._suppress = arg
      return property(**locals( ))
