from abjad.formatter.slots import _FormatterSlotsInterface


class _ContainerFormatterSlotsInterface(_FormatterSlotsInterface):

   def __init__(self, client):
      _FormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      result = [ ]
      container = self._client._client
      result.extend(['% ' + x for x in container.comments.before])
      result.extend(container.directives.before)
      return result

   @property
   def slot_2(self):
      result = [ ]
      if self._client._client.parallel:
         result.append('<<')
      else:
         result.append('{')
      return result

   @property
   def slot_3(self):
      result = [ ]
      container = self._client._client
      result.extend(container.directives.opening)
      result.extend(container.interfaces.overrides)
      result.extend(container.interfaces.opening)
      return ['\t' + x for x in result]

   @property
   def slot_4(self):
      return self._client._contents

   @property
   def slot_5(self):
      result = [ ]
      container = self._client._client
      result.extend(container.interfaces.closing)
      result.extend(container.interfaces.reverts)
      result.extend(container.directives.closing)
      return ['\t' + x for x in result]

   @property
   def slot_6(self):
      result = [ ]
      if self._client._client.parallel:
         result.append('>>')
      else:
         result.append('}')
      return result

   @property
   def slot_7(self):
      result = [ ]
      container = self._client._client
      result.extend(container.directives.after)
      result.extend(['% ' + x for x in container.comments.after])
      return result
