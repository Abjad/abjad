from abjad.container.container import _ContainerFormatter


class _ContextFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def closing(self):
      result = [ ]
      result.extend(self._client.interfaces.closing)
      return ['\t' + x for x in result]

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
      client = self._client
      result = [ ]
      if client.parallel:
         brackets_open = '<<'
      else:
         brackets_open = '{'
      overrides = client.interfaces.overrides
      if overrides:
         result.append(self.INVOCATION + ' \with {')
         result.extend(['\t' + x for x in overrides])
         result.append('} %s' % brackets_open)
      else:
         result.append(self.INVOCATION + ' %s' % brackets_open)
      return result

   @property
   def opening(self):
      result = [ ]
      result.extend(self._client.interfaces.opening)
      return ['\t' + x for x in result]
