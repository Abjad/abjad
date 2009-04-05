from abjad.container.number import _ContainerFormatterNumberInterface
from abjad.core.formatter import _Formatter


class _ContainerFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)
      self._number = _ContainerFormatterNumberInterface(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def contents(self):
      result = [ ]
      for m in self._client._music:
         result.extend(m.format.split('\n'))
      result = ['\t' + x for x in result]
      return result

   @property
   def number(self):
      return self._number

   @property
   def slot_1(self):
      result = [ ]
      client = self._client
      result.extend(['% ' + x for x in client.comments.before])
      result.extend(client.directives.before)
      return result

   @property
   def slot_2(self):
      result = [ ]
      if self._client.parallel:
         result.append('<<')
      else:
         result.append('{')
      return result

   @property
   def slot_3(self):
      result = [ ]
      client = self._client
      result.extend(client.directives.opening)
      result.extend(client.interfaces.overrides)
      result.extend(client.interfaces.opening)
      return ['\t' + x for x in result]

   @property
   def slot_4(self):
      return self.contents

   @property
   def slot_5(self):
      result = [ ]
      client = self._client
      result.extend(client.interfaces.closing)
      result.extend(client.interfaces.reverts)
      result.extend(client.directives.closing)
      return ['\t' + x for x in result]

   @property
   def slot_6(self):
      result = [ ]
      if self._client.parallel:
         result.append('>>')
      else:
         result.append('}')
      return result

   @property
   def slot_7(self):
      result = [ ]
      client = self._client
      result.extend(client.directives.after)
      result.extend(['% ' + x for x in client.comments.after])
      return result
