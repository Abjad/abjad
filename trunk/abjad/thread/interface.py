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
      signature = _ContainmentSignature( )
      signature._self = self._client._ID
      for component in self._client.parentage.parentage:
         if isinstance(component, Voice) and not signature._voice:
            signature._voice = component._ID
         elif isinstance(component, Staff) and not signature._staff:
            numeric_id = '%s-%s' % (
               component.__class__.__name__, id(component))
            signature._staff = numeric_id
         elif isinstance(component, Score) and not signature._score:
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
