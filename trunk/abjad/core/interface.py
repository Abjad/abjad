from abjad.core.abjadcore import _Abjad


class _Interface(_Abjad):

   def __init__(self, client):
      self._client = client

#   ### PRIVATE METHODS ###
#
#   def _copy(self):
#      from copy import copy
#      client = self._client
#      self._client = None
#      result = copy(self)
#      self._client = client
#      return result
