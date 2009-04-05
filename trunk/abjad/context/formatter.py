from abjad.container.container import _ContainerFormatter


class _ContextFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def INVOCATION(self):
      client = self._client
      if client.name is not None:
         return r'\context %s = "%s"' % (client.context, client.name)
      else:
          return r'\new %s' % client.context

   @property
   def slot_2(self):
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
   def slot_3(self):
      result = [ ]
      client = self._client
      result.extend(client.interfaces.opening)
      return ['\t' + x for x in result]

   @property
   def slot_5(self):
      result = [ ]
      client = self._client
      result.extend(client.interfaces.closing)
      return ['\t' + x for x in result]
