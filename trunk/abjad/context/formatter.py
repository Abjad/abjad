from .. containers.container import _ContainerFormatter

class _ContextFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)

#   @property
#   def _invocation(self):
#      result = [ ]
#      result.extend(self._client.invocation._opening)
#      if self.variable is not None:
#         result[0] = '%s = %s' % (self.variable, result[0])
#      return result

   @property
   def _invocation_opening(self):
      return self._client.invocation._opening

   @property
   def _invocation_closing(self):
      return self._client.invocation._closing


### NOTE: this is now identical to _ContainerFormatter.lily( )
#   @property
#   def lily(self):
#      result = [ ]
#      result.extend(self._client.comments._before)
#      result.extend(self.before)
#      result.extend(self._invocation_opening)
#      result.extend(self.opening)
#      result.extend(self._opening)
#      result.extend(self._contents)
#      result.extend(self._closing)
#      result.extend(self.closing)
##      result.extend(self._client.invocation._closing)
#      result.extend(self._invocation_closing)
#      result.extend(self.after)
#      result.extend(self._client.comments._after)
#      return '\n'.join(result)
