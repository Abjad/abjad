from abjad.components.Container.formatter import _ContainerFormatter
from abjad.components.Cluster.slots import _ClusterFormatterSlotsInterface


class _ClusterFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self._slots = _ClusterFormatterSlotsInterface(self) 

   ## PUBLIC ATTRIBUTES ##

   @property
   def cluster(self):
      return self._client
   
   @property
   def slots(self):
      return self._slots
