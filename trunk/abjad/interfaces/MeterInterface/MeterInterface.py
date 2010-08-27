#from abjad.interfaces._BacktrackingInterface import _BacktrackingInterface
from abjad.interfaces._Interface import _Interface
#from abjad.interfaces._ObserverInterface import _ObserverInterface
#from abjad.core import Rational
#from abjad.tools.metertools import Meter
#from abjad.tools import durtools


class MeterInterface(_Interface):

   __slots__ = ('_client')

   def __init__(self, _client):
      _Interface.__init__(self, _client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      from abjad.tools.marktools.get_effective_time_signature import get_effective_time_signature
      from abjad.components.Measure._Measure import _Measure
      from abjad.tools import measuretools
      explicit_meter = getattr(self._client, '_explicit_meter', None)
      if explicit_meter is not None:
         return explicit_meter
      else:
         return get_effective_time_signature(self._client)
#      if isinstance(self._client, _Measure):
#         if isinstance(self._client, measuretools.DynamicMeasure):
#            self._client._update_explicit_meter( )
#         return self._client._explicit_meter
#      else:
#         return get_effective_time_signature(self._client)



#class MeterInterface(_ObserverInterface, _BacktrackingInterface):
#   '''Publish information about effective and forced meter.
#   '''
#   
#   __slots__ = ('_acceptable_types', '_default', '_effective', '_forced', 
#      '_interface_name', '_suppress')
#
#   def __init__(self, _client, _update_interface):
#      _ObserverInterface.__init__(self, _client, _update_interface)
#      _BacktrackingInterface.__init__(self, 'meter')
#      self._acceptable_types = (Meter, )
#      self._default = Meter(4, 4)
#      self._forced = None
#      #self._suppress = False
#      self._suppress = None
#
#   ## TODO: Generalize _self_should_contribute for both _Clef and _Meter ##
#
#   ## PRIVATE ATTRIBUTES ##
#
#   @property
#   def _opening(self):
#      '''Format contributions at container opening or before leaf.'''
#      result = [ ]
#      if self._self_should_contribute:
#         effective_meter = self.effective
#         result.append(effective_meter.format)
#         partial = effective_meter.partial
#         if partial is not None:
#            string = durtools.assignable_rational_to_lilypond_duration_string(partial)
#            result.append(r'\partial %s' % string)
#      return result
#
#   @property
#   def _parent_can_contribute(self):
#      r'''True when any parent, other than self, can contribute LP \time.'''
#      for parent in self._client.parentage.proper_parentage:
#         try:
#            if parent.meter._self_can_contribute:
#               return True
#         except AttributeError:
#            pass
#      return False
#
#   @property
#   def _self_can_contribute(self):
#      r'''True when self is able to contribute LilyPond \time.'''
#      return not self.suppress and (self.forced or self.change)
#
#   @property
#   def _self_should_contribute(self):
#      r'''True when self should contribute LilyPond \time.'''
#      return self._self_can_contribute and not self._parent_can_contribute
#
#   ## PUBLIC ATTRIBUTES ##
#
#   @property
#   def default(self):
#      return self._default
#
#   @apply
#   def suppress( ):
#      r'''Read / write attribute to suppress contribution
#         of LilyPond \time indication at format-time.'''
#      def fget(self):
#         return self._suppress
#      def fset(self, arg):
#         assert isinstance(arg, (bool, type(None)))
#         self._suppress = arg
#      return property(**locals( ))
