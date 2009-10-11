from abjad.core.backtracking import _BacktrackingInterface
from abjad.core.grobhandler import _GrobHandler
from abjad.core.observer import _Observer
from abjad.meter.meter import Meter
import types


class MeterInterface(_Observer, _GrobHandler, _BacktrackingInterface):
   '''Handle LilyPond TimeSignature grob.
      Publish information about effective and forced meter.'''
   
   def __init__(self, _client, _updateInterface):
      '''Bind client, set forced to None and suppress to False.'''
      _Observer.__init__(self, _client, _updateInterface)
      _GrobHandler.__init__(self, 'TimeSignature')
      _BacktrackingInterface.__init__(self, 'meter')
      self._acceptableTypes = (Meter, )
      self._default = Meter(4, 4)
      self._forced = None
      self._suppress = False

   ## TODO: Generalize _selfShouldContribute for both _Clef and _Meter ##

   ## PRIVATE ATTRIBUTES ##

   @property
   def _selfCanContribute(self):
      r'''True when self is able to contribute LilyPond \time.'''
      return not self.suppress and (self.forced or self.change)

   @property
   def _selfShouldContribute(self):
      r'''True when self should contribute LilyPond \time.'''
      return self._selfCanContribute and not self._parentCanContribute

   @property
   def _parentCanContribute(self):
      r'''True when any parent, other than self, can contribute LP \time.'''
      #for parent in self.client.parentage.parentage[1:]:
      for parent in self._client.parentage.parentage[1:]:
         try:
            if parent.meter._selfCanContribute:
               return True
         except AttributeError:
            pass
      return False

   ## PUBLIC ATTRIBUTES ##

   @property
   def default(self):
      return self._default

   @property
   def _opening(self):
      '''Format contributions at container opening or before leaf.'''
      result = [ ]
      if self._selfShouldContribute:
         result.append(self.effective.format)
      return result

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
