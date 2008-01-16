from .. core.formatter import _Formatter

class ContainerFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)

   @property
   def _contents(self):
      result = [ ]
      for m in self._client._music:
         result.extend(m.format.split('\n'))
      result = ['\t' + x for x in result]
      return result

   @property
   def lily(self):
      result = [ ]
      result.extend(self._client.comments.before)
      result.extend(self.before)
      result.extend(self._contents)
      result.extend(self._client.barline._closing)
      result.extend(self.after)
      return '\n'.join(result)
