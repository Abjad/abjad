from abjad.core.abjadcore import _Abjad


class _Interface(_Abjad):

   def __init__(self, client):
      self._client = client

   ## PUBLIC ATTRIBUTES ##

   @property
   def client(self):
      return self._client
