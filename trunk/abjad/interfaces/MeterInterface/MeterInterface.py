from abjad.core import _BacktrackingInterface
from abjad.interfaces._Observer import _Observer
from abjad.core import Rational
from abjad.tools.metertools import Meter
from abjad.tools import durtools
import types


class MeterInterface(_Observer, _BacktrackingInterface):
   '''Publish information about effective and forced meter.
   '''
   
   def __init__(self, _client, _updateInterface):
      _Observer.__init__(self, _client, _updateInterface)
      _BacktrackingInterface.__init__(self, 'meter')
      self._acceptableTypes = (Meter, )
      self._default = Meter(4, 4)
      self._forced = None
      #self._suppress = False
      self._suppress = None

   ## TODO: Generalize _self_should_contribute for both _Clef and _Meter ##

   ## PRIVATE ATTRIBUTES ##

   @property
   def _opening(self):
      '''Format contributions at container opening or before leaf.'''
      result = [ ]
      if self._self_should_contribute:
         effective_meter = self.effective
         result.append(effective_meter.format)
         partial = effective_meter.partial
         if partial is not None:
            string = durtools.assignable_rational_to_lilypond_duration_string(partial)
            result.append(r'\partial %s' % string)
      return result

   @property
   def _parent_can_contribute(self):
      r'''True when any parent, other than self, can contribute LP \time.'''
      for parent in self._client.parentage.parentage[1:]:
         try:
            if parent.meter._self_can_contribute:
               return True
         except AttributeError:
            pass
      return False

   @property
   def _self_can_contribute(self):
      r'''True when self is able to contribute LilyPond \time.'''
      return not self.suppress and (self.forced or self.change)

   @property
   def _self_should_contribute(self):
      r'''True when self should contribute LilyPond \time.'''
      return self._self_can_contribute and not self._parent_can_contribute

   ## PUBLIC ATTRIBUTES ##

   @property
   def default(self):
      return self._default

   @apply
   def suppress( ):
      r'''Read / write attribute to suppress contribution
         of LilyPond \time indication at format-time.'''
      def fget(self):
         return self._suppress
      def fset(self, arg):
         assert isinstance(arg, (bool, type(None)))
         self._suppress = arg
      return property(**locals( ))
