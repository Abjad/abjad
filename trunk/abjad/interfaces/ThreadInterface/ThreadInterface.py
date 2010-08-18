from abjad.interfaces._Interface import _Interface
from abjad.interfaces.ParentageInterface.containment import _ContainmentSignature


## TODO: move to threadtools.component_to_thread_signature
class ThreadInterface(_Interface):
   '''Serve thread parentage information about component.
      Handle no LilyPond grob.'''

   def __init__(self, client):
      '''Bind to client.'''
      _Interface.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def signature(self):
      '''Return _ContainmentSignature giving the root and
         first voice, staff and score in parentage of component.'''
      from abjad.components.Score import Score
      from abjad.tools.scoretools import StaffGroup
      from abjad.components.Staff import Staff
      from abjad.components.Voice import Voice
      signature = _ContainmentSignature( )
      signature._self = self._client._ID
      for component in self._client.parentage.parentage:
         if isinstance(component, Voice) and not signature._voice:
            signature._voice = component._ID
         elif isinstance(component, Staff) and not signature._staff:
            numeric_id = '%s-%s' % (
               component.__class__.__name__, id(component))
            signature._staff = numeric_id
         elif isinstance(component, StaffGroup) and not signature._staffgroup:
            signature._staffgroup = component._ID
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
