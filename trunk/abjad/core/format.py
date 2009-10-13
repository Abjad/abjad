from abjad.interfaces.interface.interface import _Interface


class _FormatInterface(_Interface):

   def __init__(self, _client):
      self._client = _client

   ## PUBLIC ATTRIBUTES ##

   @property
   def interface(self):
      return self._client
