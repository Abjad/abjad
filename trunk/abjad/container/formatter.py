from abjad.container.number import _ContainerFormatterNumberInterface
from abjad.core.formatter import _Formatter


class _ContainerFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)
      self._number = _ContainerFormatterNumberInterface(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def closing(self):
      result = [ ]
      client = self._client
      interfaces = client.interfaces
      if not hasattr(client, 'context'):
         result.extend(interfaces.reverts)
      result.extend(interfaces.closing)
      return ['\t' + x for x in result]

   @property
   def contents(self):
      result = [ ]
      for m in self._client._music:
         result.extend(m.format.split('\n'))
      result = ['\t' + x for x in result]
      return result
   
   @property
   def format(self):
      client = self._client
      annotations = client.annotations
      comments = client.comments
      interfaces = client.interfaces
      result = [ ]
      result.extend(['% ' + x for x in comments.before])
      result.extend(annotations.before)
      result.extend(self.invocation_opening)
      result.extend(annotations.opening)
      result.extend(self.opening)
      result.extend(self.contents)
      result.extend(self.closing)
      result.extend(annotations.closing)
      result.extend(self.invocation_closing)
      result.extend(annotations.after)
      result.extend(['% ' + x for x in comments.after])
      return '\n'.join(result)

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
      result = [ ]
      if self._client.parallel:
         result.append('<<')
      else:
         result.append('{')
      return result

   @property
   def number(self):
      return self._number

   @property
   def opening(self):
      result = [ ]
      client = self._client
      interfaces = client.interfaces
      if not hasattr(client, 'context'):
         result.extend(interfaces.overrides)
      result.extend(interfaces.opening)
      return ['\t' + x for x in result]
