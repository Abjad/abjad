from abjad.core.interface import _Interface
from abjad.parentage.containment import _ContainmentSignature


class _ThreadInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def signature(self):
      '''Return _ContainmentSignature giving the root and
         first voice, staff and score in parentage of component.'''
      from abjad.score.score import Score
      from abjad.staff.staff import Staff
      from abjad.voice.voice import Voice
      from abjad.helpers.is_less_than_voice import _is_less_than_voice
      signature = _ContainmentSignature( )
      signature._self = self._client._ID
      found_less_than_voice = False
      for component in self._client.parentage.parentage:
         if _is_less_than_voice(component):
            found_less_than_voice = True 
         if isinstance(component, Voice) and not signature._voice:
            signature._voice = component._ID
         if isinstance(component, Staff) and not signature._staff:
            signature._staff = component._ID
            if found_less_than_voice and not signature._voice:
               numeric_id = '%s-%s' % (
                  component.__class__.__name__, id(component))
               signature._voice = numeric_id
         if isinstance(component, Score) and not signature._score:
            signature._score = component._ID
      else:
         '''Root components must be manifestly equal to compare True.'''
         signature._root = id(component)
         signature._root_str = component._ID
      return signature

   ## PUBLIC METHODS ##

   def report(self):
      '''Print thread signature to the interpreter.'''
      print self.signature
