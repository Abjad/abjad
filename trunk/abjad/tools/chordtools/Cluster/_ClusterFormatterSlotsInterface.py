from abjad.components.Container._ContainerFormatterSlotsInterface import \
   _ContainerFormatterSlotsInterface


class _ClusterFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_2(self):
      result = [ ]
      cluster = self.formatter.cluster
      #contributor = (cluster.brackets, 'open')
      #contributions = [r'\makeClusters %s' % cluster.brackets.open[0]]
      contributor = ('cluster_brackets', 'open')
      if self._client._client.parallel:
         brackets_open = ['<<']
      else:
         brackets_open = ['{']
      contributions = [r'\makeClusters %s' % brackets_open[0]]
      result.append([contributor, contributions])
      return tuple(result)
