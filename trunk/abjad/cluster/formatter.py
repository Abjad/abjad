from abjad.container.formatter import _ContainerFormatter
from abjad.cluster.slots import _ClusterFormatterSlotsInterface


class _ClusterFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self._slots = _ClusterFormatterSlotsInterface(self) 

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def slots(self):
      return self._slots

#   @property
#   #def invocation_opening(self):
#   def slot_2(self):
#      result = [r'\makeClusters ']
#      if self._client.parallel:
#         result[0] += '<<'
#      else:
#         result[0] += '{'
#      return result
