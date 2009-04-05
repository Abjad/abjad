from abjad.core.formatcarrier import _FormatCarrier
from abjad.formatter.formatter import _Formatter
from abjad.leaf.number import _LeafFormatterNumberInterface
from abjad.leaf.slots import _LeafFormatterSlotsInterface


class _LeafFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)
      self._number = _LeafFormatterNumberInterface(self)
      self._slots = _LeafFormatterSlotsInterface(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def agrace(self):
      result = [ ]
      agrace = self._client.grace.after
      if len(agrace) > 0:
         result.append(agrace.format)
      return result

   @property
   def agrace_opening(self):
      if len(self._client.grace.after) > 0:
         return [r'\afterGrace']
      else:
         return [ ] 

   @property
   def clef(self):
      result = [ ]
      if hasattr(self._client, '_clef'):
         result.append(self._client._clef.format)
      return result

   @property
   def grace(self):
      result = [ ]
      grace = self._client.grace.before
      if len(grace) > 0:
         result.append(grace.format)
      return result

   @property
   def leaf_body(self):
      result = [ ]
      client = self._client
      directives = client.directives
      interfaces = client.interfaces
      spanners = client.spanners
      result.extend(directives.left)
      result.extend(spanners.left)
      result.extend(interfaces.left)
      result.extend(self.nucleus)
      result.extend(self.tremolo)
      result.extend(interfaces.right)
      result.extend(spanners.right)
      result.extend(directives.right)
      result.extend(self.number_contribution)
      result.extend(['% ' + x for x in client.comments.right])
      return [' '.join(result)]

   @property
   def nucleus(self):
      return self._client.body

   @property
   def number(self):
      return self._number

   @property
   def number_contribution(self):
      result = [ ]
      client = self._client
      contribution = self.number._leaf_contribution
      if contribution == 'markup':
         result.append(r'^ \markup { %s }' % client.numbering.leaf)
      elif contribution == 'comment':
         result.append(r'%% leaf %s' % client.numbering.leaf)
      return result

   @property
   def tremolo(self):
      result = [ ]
      subdivision = self._client.tremolo.subdivision
      if subdivision:
         result.append(':%s' % subdivision) 
      return result
