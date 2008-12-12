from abjad.core.interface import _Interface
from abjad.helpers.instances import instances


class _VoiceInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)

      
   ### PRIVATE ATTRIBUTES ###

   @property
   def _canBeContainedInVoice(self):
      client = self._client
      if client.kind('Voice'):
         return True
      elif not hasattr(client, 'invocation'):
         if not getattr(client, 'parallel', False):
            return True
      return False

   ### TODO - make instances return a generator
   @property
   def _containsVoiceBreaker(self):
      for x in instances(self._client, '_Component'):
         if not x.voice._canBeContainedInVoice:
            return True
      else:
         return False

   ### PUBLIC ATTRIBUTES ###

   @property
   def creator(self):
      client = self._client
      if not self._canBeContainedInVoice:
         return None
      else:
         parentage = self._client._parentage._iparentage
         for i, p in enumerate(parentage):
            if hasattr(p, 'invocation'):
               return p
            elif getattr(p, 'parallel', False):
               return parentage[i - 1]
         else:
            return None
         
   @property
   def effective(self):
      creator = self.creator
      if creator is not None and creator.kind('Voice'):
         return creator
      else:
         return None

   @property
   def explicit(self):
      return bool(self.effective)      

   @property
   def name(self):
      effective = self.effective
      if effective:
         return effective.invocation.name
      else:
         return None

   @property
   def signature(self):
      name = self.name
      if name:
         return (name, )
      else:
         creator = self.creator
         if creator:
            return (id(creator), )
         elif self._client.kind('Container') and \
            self._canBeContainedInVoice and not self._containsVoiceBreaker:
            return (-1, )
         elif self._client._parentage._first('Container') is not None and \
            not self._containsVoiceBreaker:
            return (-1, )
         else:
            return None
