from abjad.core import _BacktrackingInterface
from abjad.core import _GrobHandler
from abjad.core import _Observer
from abjad.marks import KeySignature
import types


class KeySignatureInterface(_Observer, _GrobHandler, _BacktrackingInterface):
   '''Handle LilyPond KeySignature grob.
   Publish information about effective and forced key_signature.'''
   
   def __init__(self, _client, _updateInterface):
      '''Bind client, set forced to None and suppress to False.'''
      _Observer.__init__(self, _client, _updateInterface)
      _GrobHandler.__init__(self, 'KeySignature')
      _BacktrackingInterface.__init__(self, 'key_signature')
      self._acceptableTypes = (KeySignature, )
      #self._default = KeySignature('c', 'major')
      self._default = None
      self._forced = None
      #self._suppress = False
      self._suppress = None

   ## TODO: Generalize _self_should_contribute for both _Clef and _Meter ##

   ## PRIVATE ATTRIBUTES ##

   @property
   def _self_can_contribute(self):
      r'''True when self is able to contribute LilyPond stuff.'''
      return not self.suppress and (self.forced or self.change)

   @property
   def _self_should_contribute(self):
      r'''True when self should contribute LilyPond staff.'''
      return self._self_can_contribute and not self._parent_can_contribute

   @property
   def _parent_can_contribute(self):
      r'''True when any parent, other than self, can contribute LP \time.'''
      for parent in self._client.parentage.parentage[1:]:
         try:
            if parent.key_signature._self_can_contribute:
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
      if self._self_should_contribute:
         result.append(self.effective.format)
      return result

   @apply
   def suppress( ):
      r'''Read / write attribute to suppress contribution
      of LilyPond \key indication at format-time.'''
      def fget(self):
         return self._suppress
      def fset(self, arg):
         assert isinstance(arg, (bool, types.NoneType))
         self._suppress = arg
      return property(**locals( ))
