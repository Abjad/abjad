from abjad.component.formatter import _ComponentFormatter
from abjad.leaf.number import _LeafFormatterNumberInterface
from abjad.leaf.slots import _LeafFormatterSlotsInterface


class _LeafFormatter(_ComponentFormatter):

   def __init__(self, client):
      _ComponentFormatter.__init__(self, client)
      self._number = _LeafFormatterNumberInterface(self)
      self._slots = _LeafFormatterSlotsInterface(self)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _agrace_body(self):
      result = [ ]
      agrace = self._client.grace.after
      if len(agrace):
         result.append(agrace.format)
      return result

   @property
   def _agrace_opening(self):
      result = [ ]
      if len(self._client.grace.after):
         result.append(r'\afterGrace')
      return result

   @property
   def _grace_body(self):
      result = [ ]
      grace = self._client.grace.before
      if len(grace):
         result.append(grace.format)
      return result

   @property
   def _leaf_body(self):
      result = [ ]
      client = self._client
      directives = client.directives
      interfaces = client.interfaces
      spanners = client.spanners
      #result.extend(directives.left)
      result.extend(spanners.left)
      result.extend(interfaces.left)
      result.extend(self._nucleus)
      result.extend(self._tremolo_subdivision_contribution)
      result.extend(interfaces.right)
      result.extend(spanners._right)
      result.extend(directives.right)
      result.extend(self._number_contribution)
      result.extend(['% ' + x for x in client.comments.right])
      return [' '.join(result)]

   @property
   def _nucleus(self):
      return self._client.body

   @property
   def _number_contribution(self):
      result = [ ]
      leaf = self._client
      contribution = self.number._leaf_contribution
      if contribution == 'markup':
         result.append(r'^ \markup { %s }' % leaf.number)
      elif contribution == 'comment':
         result.append(r'%% leaf %s' % leaf.number)
      return result

   @property
   def _tremolo_subdivision_contribution(self):
      result = [ ]
      subdivision = self._client.tremolo.subdivision
      if subdivision:
         result.append(':%s' % subdivision) 
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def leaf(self):
      return self._client

   @property
   def number(self):
      return self._number

   @property
   def slots(self):
      return self._slots
