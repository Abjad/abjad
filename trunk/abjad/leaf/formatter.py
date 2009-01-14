from abjad.core.formatter import _Formatter
from abjad.core.formatcarrier import _FormatCarrier


class _LeafFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)
      self.left = [ ]
      self.right = [ ]

   ### PRIVATE ATTRIBUTES ###

   @property
   def _agrace(self):
      result = [ ]
      agrace = self._client.grace.after
      if len(agrace) > 0:
         result.append(agrace.format)
      return result

   @property
   def _agrace_opening(self):
      if len(self._client.grace.after) > 0:
         return [r'\afterGrace']
      else:
         return [ ] 

   @property
   def _body(self):
      result = [ ]
      result.extend(self.left)
      result.extend(self._collectLocation('_left'))
### NOTE: What was this for? VA
#      if hasattr(self._client, 'notehead') and \
#         self._client.notehead is not None:
#         result.extend(self._client.notehead._formatter.left)
      result.append(self._client._body)
      result.extend(self._client.tremolo.body)
      result.extend(self._collectLocation('_right'))
      result.extend(self.right)
      result.extend(self._number)
      result.extend(self._client.comments._right)
      return [' '.join(result)]

   @property
   def _clef(self):
      result = [ ]
      if hasattr(self._client, '_clef'):
         result.append(self._client._clef.format)
      return result

   @property
   def _grace(self):
      result = [ ]
      grace = self._client.grace.before
      if len(grace) > 0:
         result.append(grace.format)
      return result

   @property
   def _number(self):
      result = [ ]
      #if self.number or self._client._parentage._number:
      if self.number or self._client.parentage._number:
         result.append(r'^ \markup { %s }' % self._client.number)
      return result

   ### PUBLIC ATTRIBUTES ###

   ### NOTE - clef *must* come lexically before set-octavation ###

   @property
   #def lily(self):
   def format(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      result.extend(self._grace)
      #result.extend(self._clef)
      result.extend(self._grobOverrides)
      result.extend(self._collectLocation('_before'))
      result.extend(self._agrace_opening)
      result.extend(self._body)
      result.extend(self._agrace)
      result.extend(self._collectLocation('_after'))
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return '\n'.join(result)
