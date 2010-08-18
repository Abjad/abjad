from abjad.interfaces._Interface import _Interface
from abjad.interfaces.OffsetInterface.OffsetProlatedInterface import OffsetProlatedInterface
from abjad.interfaces.OffsetInterface._OffsetSecondsInterface import _OffsetSecondsInterface
from abjad.core import Rational


## TODO: if no way to get rid of OffsetInterface, at least get rid of nested interfaces
class OffsetInterface(_Interface):
   '''Offset interface.
   '''

   def __init__(self, _client, _updateInterface):
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

#   @property
#   def prolated_start(self):
#      pass
#
#   @property
#   def prolated_stop(self):
#      pass
