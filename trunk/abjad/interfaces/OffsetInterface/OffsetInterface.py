from abjad.interfaces._Interface import _Interface
from abjad.interfaces.OffsetInterface.OffsetProlatedInterface import OffsetProlatedInterface
from abjad.interfaces.OffsetInterface._OffsetSecondsInterface import _OffsetSecondsInterface
from abjad.core import Rational


class OffsetInterface(_Interface):
   '''Namespace only to hold rational-valued start and stop offsets.'''

   def __init__(self, _client, _updateInterface):
      '''Bind to client.
         Pass update interface reference to aggregated interfaces.'''
      _Interface.__init__(self, _client)
      self._prolated = OffsetProlatedInterface(self, _updateInterface)
      self._seconds = _OffsetSecondsInterface(self, _updateInterface)

   ## PUBLIC ATTRIBUTES ##

   @property
   def prolated(self):
      return self._prolated
  
   @property
   def seconds(self):
      return self._seconds
