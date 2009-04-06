from abjad.component.slots import _ComponentFormatterSlotsInterface


class _ContainerFormatterSlotsInterface(_ComponentFormatterSlotsInterface):

   def __init__(self, client):
      _ComponentFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      result = [ ]
      container = self._client._client
      result.extend(['% ' + x for x in container.comments.before])
      result.extend(container.directives.before)
      return tuple(result)

   @property
   def slot_2(self):
      result = [ ]
      result.append(self.formatter.container.brackets.open)
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      container = self._client._client
      result.extend(['% ' + x for x in container.comments.opening])
      result.extend(container.directives.opening)
      result.extend(container.interfaces.overrides)
      result.extend(container.interfaces.opening)
      result = ['\t' + x for x in result]
      return tuple(result)

   @property
   def slot_4(self):
      return tuple(self._client._contents)

   @property
   def slot_5(self):
      result = [ ]
      container = self._client._client
      result.extend(container.interfaces.closing)
      result.extend(container.interfaces.reverts)
      result.extend(container.directives.closing)
      result.extend(['% ' + x for x in container.comments.closing])
      result = ['\t' + x for x in result]
      return tuple(result)

   @property
   def slot_6(self):
      result = [ ]
      result.append(self.formatter.container.brackets.close)
      return tuple(result)

   @property
   def slot_7(self):
      result = [ ]
      container = self._client._client
      result.extend(container.directives.after)
      result.extend(['% ' + x for x in container.comments.after])
      return tuple(result)
