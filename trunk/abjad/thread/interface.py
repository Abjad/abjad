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
            numeric_id = '%s-%s' % (
               component.__class__.__name__, id(component))
            signature._staff = numeric_id
#            signature._staff = component._ID
#            if found_less_than_voice and not signature._voice:
#               numeric_id = '%s-%s' % (
#                  component.__class__.__name__, id(component))
#               signature._voice = numeric_id
         if isinstance(component, Score) and not signature._score:
            signature._score = component._ID
      else:
         '''Root components must be manifestly equal to compare True.'''
         signature._root = id(component)
         signature._root_str = component._ID
      return signature

#   @property
#   def signature(self):
#      '''Return _ContainmentSignature giving the root and
#         first voice, staff and score in parentage of component.'''
#      from abjad.container.container import Container
#      from abjad.context.context import _Context
#      from abjad.score.score import Score
#      from abjad.staff.staff import Staff
#      from abjad.tuplet.tuplet import _Tuplet
#      from abjad.voice.voice import Voice
#      from abjad.helpers.is_less_than_voice import _is_less_than_voice
#      signature = _ContainmentSignature( )
#      signature._self = self._client._ID
#      parentage = self._client.parentage.parentage
#      '''Root components must be manifestly equal to compare True.'''
#      root = parentage[-1]
#      signature._root = id(root)
#      signature._root_str = root._ID
#      last_container = None
#      last_context = root
#      found_voice = False
#      last_parallel = None
#
#      for component in reversed(parentage):
#
#         if _is_less_than_voice(component):
#            if not found_voice:
##               if root is last_container and root.parallel:
##                     signature._voice = component._ID
##               else:
#               numeric_id = '%s-%s' % (
#                  last_context.__class__.__name__, id(last_context))
#               signature._voice = numeric_id
#
#         elif isinstance(component, Voice):
#            signature._voice = component._ID
#            found_voice = True
#
#         elif isinstance(component, Staff):
#            signature._staff = component._ID
#
#         elif isinstance(component, Score):
#            signature._score = component._ID
#
#         if isinstance(component, _Context):
#            last_context = component
#
#         if isinstance(component, Container):
#            last_container = component
#
#      return signature


   ## PUBLIC METHODS ##

   def report(self):
      '''Print thread signature to the interpreter.'''
      print self.signature
