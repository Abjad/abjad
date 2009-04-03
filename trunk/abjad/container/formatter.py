from abjad.container.number import _ContainerFormatterNumberInterface
from abjad.core.formatter import _Formatter


class _ContainerFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)
      #self.closing = [ ]
      #self.opening = [ ]
      self._number = _ContainerFormatterNumberInterface(self)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents(self):
      result = [ ]
      for m in self._client._music:
         result.extend(m.format.split('\n'))
      result = ['\t' + x for x in result]
      return result
   
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
      if self._client.parallel:
         result.append('<<')
      else:
         result.append('{')
      return result

   @property
   def _opening(self):
      result = [ ]
      client = self._client
      if not hasattr(client, 'context'):
         result.extend(self._grobOverrides)
      result.extend(self._collectLocation('_opening'))
      return ['\t' + x for x in result]

   @property
   def _closing(self):
      result = [ ]
      client = self._client
      if not hasattr(client, 'context'):
         result.extend(self._grobReverts)
      result.extend(self._collectLocation('_closing'))
      return ['\t' + x for x in result]

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      client = self._client
      annotations = client.annotations
      comments = client.comments
      result = [ ]
      result.extend(comments._before)
      #result.extend(self.before)
      result.extend(annotations.before)
      result.extend(self._invocation_opening)
      #result.extend(self.opening)
      result.extend(annotations.opening)
      result.extend(self._opening)
      result.extend(self._contents)
      result.extend(self._closing)
      #result.extend(self.closing)
      result.extend(annotations.closing)
      result.extend(self._invocation_closing)
      #result.extend(self.after)
      result.extend(annotations.after)
      result.extend(comments._after)
      return '\n'.join(result)

   @property
   def number(self):
      return self._number
