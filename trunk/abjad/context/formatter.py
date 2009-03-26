from abjad.container.container import _ContainerFormatter


class _ContextFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _invocation_closing(self):
      result = [ ]
      if self._client.parallel:
         result.append('>>')
      else:
         result.append('}')
      return result

   @property
   def _invocation_opening(self):
      result = [ ]
      invocation = self._client.invocation._invocation
      if self._client.parallel:
         brackets_open = '<<'
      else:
         brackets_open = '{'
      overrides = self._grobOverrides
      if overrides:
         result.append(invocation + ' \with {')
         result.extend(['\t' + x for x in overrides])
         result.append('} %s' % brackets_open)
      else:
         result.append(invocation + ' %s' % brackets_open)
      return result
