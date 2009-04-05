from abjad.component.slots import _ComponentFormatterSlotsInterface


class _LeafFormatterSlotsInterface(_ComponentFormatterSlotsInterface):

   def __init__(self, client):
      _ComponentFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      result = [ ]
      formatter = self._client
      leaf = formatter._client
      result.extend(formatter._grace_body)
      result.extend(['% ' + x for x in leaf.comments.before])
      result.extend(leaf.directives.before)
      result.extend(leaf.interfaces.overrides)
      result.extend(leaf.spanners.before)
      result.extend(leaf.interfaces.before)
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      formatter = self._client
      leaf = formatter._client
      result.extend(leaf.directives.opening)
      result.extend(leaf.interfaces.opening)
      result.extend(formatter._agrace_opening)
      return tuple(result)

   @property
   def slot_4(self):
      return tuple(self._client._leaf_body)

   @property
   def slot_5(self):
      result = [ ]
      formatter = self._client
      leaf = formatter._client
      result.extend(formatter._agrace_body)
      result.extend(leaf.directives.closing)
      result.extend(leaf.interfaces.closing)
      return tuple(result)

   @property
   def slot_7(self):
      result = [ ]
      formatter = self._client
      leaf = formatter._client
      result.extend(leaf.interfaces.after)
      result.extend(leaf.spanners.after)
      result.extend(leaf.directives.after)
      result.extend(['% ' + x for x in leaf.comments.after])
      return tuple(result)
