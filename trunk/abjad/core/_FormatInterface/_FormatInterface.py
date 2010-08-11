from abjad.interfaces._Interface import _Interface


class _FormatInterface(_Interface):

   def __init__(self, _client):
      self._client = _client

#   ## PUBLIC ATTRIBUTES ##
#
#   @property
#   def interface(self):
#      return self._client
