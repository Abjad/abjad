from .. containers.container import ContainerFormatter

class ContextFormatter(ContainerFormatter):

   def __init__(self, client):
      ContainerFormatter.__init__(self, client)

   @property
   def _invocation(self):
      result = [ ]
      result.extend(self._client.invocation._opening)
      if self.variable is not None:
         result[0] = '%s = %s' % (self.variable, result[0])
      return result

   @property
   def lily(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      result.extend(self._invocation)
      result.extend(self.opening)
      result.extend(self._opening)
      result.extend(self._contents)
      result.extend(self._client.barline._closing)
      result.extend(self.closing)
      result.extend(self._client.invocation._closing)
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return '\n'.join(result)
