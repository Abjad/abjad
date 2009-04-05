from abjad.container.slots import _ContainerFormatterSlotsInterface


class _ClusterFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_2(self):
      result = [r'\makeClusters ']
      if self._client._client.parallel:
         result[0] += '<<'
      else:
         result[0] += '{'
      return result
