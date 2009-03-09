from abjad.container.container import _ContainerFormatter
#from abjad.context.number import _ContextFormatterNumberInterface


class _ContextFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      #self._number = _ContextFormatterNumberInterface(self)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _invocation_closing(self):
      result = [ ]
      result.append(self._client.brackets.close)
      return result

   @property
   def _invocation_opening(self):
      result = [ ]
      invocation = self._client.invocation._invocation
      brackets = self._client.brackets
      overrides = self._grobOverrides
      if overrides:
         result.append(invocation + ' \with {')
         result.extend(['\t' + x for x in overrides])
         result.append('} %s' % brackets.open)
      else:
         result.append(invocation + ' %s' % brackets.open)
      return result

#   ## PUBLIC ATTRIBUTES ##
#
#   @property
#   def number(self):
#      return self._number
