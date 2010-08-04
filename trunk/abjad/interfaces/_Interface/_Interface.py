from abjad.core import _Abjad


class _Interface(_Abjad):

   def __init__(self, client):
      self._client = client
