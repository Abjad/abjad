from abjad.container.container import _ContainerFormatter


class _ContextFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)

#   @property
#   def _invocation_opening(self):
#      return self._client.invocation._opening
#
#   @property
#   def _invocation_closing(self):
#      return self._client.invocation._closing

   @property
   def _invocation_opening(self):
      result = [ ]
      invocation = self._client.invocation._invocation
      brackets = self._client.brackets
      #grob_overrides = self._collectLocation('_before')
      overrides = self._grobOverrides
      if overrides:
         result.append(invocation + ' \with {')
         result.extend(['\t' + x for x in overrides])
         result.append('} %s' % brackets.open)
      else:
         result.append(invocation + ' %s' % brackets.open)
      return result

   @property
   def _invocation_closing(self):
      result = [ ]
      result.append(self._client.brackets.close)
      return result
