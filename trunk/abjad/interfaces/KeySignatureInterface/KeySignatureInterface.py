from abjad.interfaces._Interface import _Interface


class KeySignatureInterface(_Interface):

   def __init__(self, _client):
      _Interface.__init__(self, _client)
      self._effective = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      from abjad.tools.marktools.get_effective_key_signature import get_effective_key_signature
      return get_effective_key_signature(self._client)
