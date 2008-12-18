from abjad.container.formatter import _ContainerFormatter

class _ClusterFormatter(_ContainerFormatter):
   
   @property
   def _invocation_opening(self):
      result = [r'\makeClusters ']
      open = self._client.brackets.open
      if open != '(':
         result[0] += open
      return result
