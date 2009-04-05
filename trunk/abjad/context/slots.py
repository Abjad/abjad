from abjad.container.slots import _ContainerFormatterSlotsInterface


class _ContextFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_2(self):
      result = [ ]
      #client = self._client
      formatter = self._client
      context = formatter._client
      if context.parallel:
         brackets_open = '<<'
      else:
         brackets_open = '{'
      overrides = context.interfaces.overrides
      if overrides:
         result.append(formatter.INVOCATION + ' \with {')
         result.extend(['\t' + x for x in overrides])
         result.append('} %s' % brackets_open)
      else:
         result.append(formatter.INVOCATION + ' %s' % brackets_open)
      return result

   @property
   def slot_3(self):
      result = [ ]
      result.extend(self._client._client.interfaces.opening)
      return ['\t' + x for x in result]

   @property
   def slot_5(self):
      result = [ ]
      result.extend(self._client._client.interfaces.closing)
      return ['\t' + x for x in result]
