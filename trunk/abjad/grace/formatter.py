from .. containers.formatter import ContainerFormatter

class GraceFormatter(ContainerFormatter):

   def __init__(self, client):
      ContainerFormatter.__init__(self, client)

   @property
   def _invocation_opening(self):
      result = [ ]
      if self._client._type == 'after':
         result.append('{')
      else:
         result.append(r'\%s {' % self._client._type)
      return result

   @property
   def _invocation_closing(self):
      result = [ ]
      result.append('}')
      return result
