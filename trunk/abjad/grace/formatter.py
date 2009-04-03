from abjad.container.formatter import _ContainerFormatter


class _GraceFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def invocation_closing(self):
      result = [ ]
      result.append('}')
      return result

   @property
   def invocation_opening(self):
      result = [ ]
      if self._client.type == 'after':
         result.append('{')
      else:
         result.append(r'\%s {' % self._client.type)
      return result
