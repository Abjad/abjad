from abjad.core.formatter import _Formatter


class _NoteHeadFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      client = self._client
      assert client.pitch
      result = [ ]
      result.extend(client.before)
      result.append(client.pitch.format)
      return '\n'.join(result)
