from abjad.container.formatter import _ContainerFormatter


class _ClusterFormatter(_ContainerFormatter):

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def invocation_opening(self):
      result = [r'\makeClusters ']
      if self._client.parallel:
         result[0] += '<<'
      else:
         result[0] += '{'
      return result
