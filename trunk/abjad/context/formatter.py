from abjad.container.container import _ContainerFormatter


class _ContextFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def INVOCATION(self):
      client = self._client
      if client.name is not None:
         return r'\context %s = "%s"' % (client.context, client.name)
      else:
          return r'\new %s' % client.context

   @property
   def invocation_closing(self):
      result = [ ]
      if self._client.parallel:
         result.append('>>')
      else:
         result.append('}')
      return result

   @property
   def invocation_opening(self):
      result = [ ]
      if self._client.parallel:
         brackets_open = '<<'
      else:
         brackets_open = '{'
      overrides = self._client.interfaces.overrides
      if overrides:
         result.append(self.INVOCATION + ' \with {')
         result.extend(['\t' + x for x in overrides])
         result.append('} %s' % brackets_open)
      else:
         result.append(self.INVOCATION + ' %s' % brackets_open)
      return result
