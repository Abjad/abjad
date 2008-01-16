from .. core.formatter import _Formatter

class NoteHeadFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)

   @property
   def _settings(self):
      result = [ ]
      # the tuple ('_', 'format') to startswith( ) is hackish;
      # we're looking for all user-defined settings and filtering out
      # private variables and the notehead formatter.
      for key, value in self._client.__dict__.iteritems( ):
         if not key.startswith(('_', 'format')) and value is not None:
            result.append((key, value))
      return result

   @property
   def _BEFORE(self):
      result = [ ]
      if self._client._client.kind('Chord'):
         if self._client.transparent:
            result.append(r"\tweak #'transparent ##t")
         if self._client.style:
            result.append(r"\tweak #'style #%s" % self._client.style)
      else:
         if self._client.transparent:
            result.append(r"\once \override NoteHead #'transparent = ##t")
         if self._client.style:
            result.append(r"\once \override NoteHead #'style = #%s" %
               self._client.style)
      return result

   @property
   def _lily(self):
      assert self._client.pitch
      result = [ ]
      result.extend(self.before)
      result.extend(self._BEFORE)
      result.append(self._client.pitch.lily)
      result.extend(self.after)
      return result

   @property
   def lily(self):
      return '\n'.join(self._lily)
