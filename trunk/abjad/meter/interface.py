from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.exceptions.exceptions import MeterAssignmentError
from abjad.helpers.in_terms_of import _in_terms_of
from abjad.meter.meter import Meter
import types


class _MeterInterface(_Interface, _GrobHandler):
   '''Handle LilyPond TimeSignature grob.
      Publish information about effective and forced meter.'''
   
   def __init__(self, client):
      '''Bind client, set forced to None and suppress to False.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'TimeSignature')
      self._forced = None
      self._suppress = False

   ## PRIVATE ATTRIBUTES ##

   @property
   def _selfCanContribute(self):
      r'''True when self is able to contribute LilyPond \time.'''
      from abjad.measure.dynamic.measure import DynamicMeasure
      if not self.suppress:
         #if isinstance(self._client, DynamicMeasure):
         if isinstance(self.client, DynamicMeasure):
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
      for parent in self.client.parentage.parentage[1:]:
         try:
            if parent.meter._selfCanContribute:
               return True
         except AttributeError:
            pass
      return False

   ## PUBLIC ATTRIBUTES ##

   @property
   def opening(self):
      '''Format contributions at container opening or before leaf.'''
      result = [ ]
      if self._selfShouldContribute:
         result.append(self.effective.format)
      return result

   ## TODO: Generalize meter and clef interfaces to _BacktrackingInterface ##
   ##       Include definition of 'change' ##

   @property
   def change(self):
      '''True if meter changes here, otherwise False.'''
      return bool(getattr(self.client, 'prev', None) and \
         self.client.prev.meter.effective != self.effective)

   ## TODO - the explicit check for DynamicMeasure seems like
   ##        a (small) hack; is there a better implementation?
   ##        Maybe this also suggests _DynamicMeasureMeterInterface

   @property
   def effective(self):
      '''Return reference to meter effectively governing client.'''
      from abjad.measure.dynamic.measure import DynamicMeasure
      #client = self._client
      client = self.client
      if isinstance(client, DynamicMeasure):
         if client.denominator:
            return Meter(
               _in_terms_of(client.duration.contents, client.denominator))
         else:
            return Meter(client.duration.contents)
      #cur = self._client
      cur = self.client
      while cur is not None:
         #if cur.meter._forced:
         #   return cur.meter._forced
         if cur.meter.forced:
            return cur.meter.forced
         else:
            #cur = cur.prev
            ## should there be explicit measure-navigation in navigator?
            #cur = cur._navigator._prevBead
            cur = getattr(cur, 'prev', None)
      #for x in self._client.parentage.parentage[1:]:
      #   if hasattr(x, 'meter') and x.meter._forced:
      #      return x.meter._forced
      for x in self.client.parentage.parentage[1:]:
         if hasattr(x, 'meter') and x.meter.forced:
            return x.meter.forced
      return Meter(4, 4)

   ## TODO: _MeterInterface instance-checking suggests _DynamicMeasureMeterInterface is needed. ##

   @apply
   def forced( ):
      '''Read / write attribute to set meter explicitly.'''
      def fget(self):
         return self._forced
      def fset(self, arg):
         ## TODO: Figure out why DynamicMeasure testing doesn't work ##
         #from measure.dynamic.measure import DynamicMeasure
         #if isinstance(self.client, DynamicMeasure):
         if self.client.__class__.__name__ == 'DynamicMeasure':
            raise MeterAssignmentError
         assert isinstance(arg, (Meter, types.NoneType))
         self._forced = arg
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
