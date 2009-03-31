from abjad.core.formatter import _Formatter
from abjad.core.formatcarrier import _FormatCarrier
from abjad.leaf.number import _LeafFormatterNumberInterface


class _LeafFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)
      self.left = [ ]
      self._number = _LeafFormatterNumberInterface(self)
      self.right = [ ]

   ## PRIVATE ATTRIBUTES ##

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
      client = self._client
      result.extend(self.left)
      result.extend(self._collectLocation('_left'))
      result.append(client._body)
      result.extend(client.tremolo.body)
      result.extend(self._collectLocation('_right'))
      result.extend(self.right)
      result.extend(self._number_contribution)
      result.extend(client.comments._right)
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
   def _number_contribution(self):
      result = [ ]
      client = self._client
      contribution = self.number._leaf_contribution
      if contribution == 'markup':
         result.append(r'^ \markup { %s }' % client.numbering.leaf)
      elif contribution == 'comment':
         result.append(r'%% leaf %s' % client.numbering.leaf)
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      result.extend(self._grace)
      result.extend(self._grobOverrides)
      result.extend(self._collectLocation('_before'))
      result.extend(self._collectLocation('_opening'))
      result.extend(self._agrace_opening)
      result.extend(self._body)
      result.extend(self._agrace)
      result.extend(self._collectLocation('_closing'))
      result.extend(self._collectLocation('_after'))
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return '\n'.join(result)

   @property
   def number(self):
      return self._number
