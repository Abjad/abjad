from abjad.core.interface import _Interface
from abjad.leaf.leaf import _LeafFormatter


class _ChordFormatter(_LeafFormatter):

   def __init__(self, client):
      _LeafFormatter.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def body(self):
      '''Return string representation of everything in body of self.'''
      client = self._client
      annotations = client.annotations
      comments = client.comments
      interfaces = client.interfaces
      spanners = client.spanners
      result = [ ]
      result.extend(annotations.left)
      result.extend(spanners.left)
      result.extend(interfaces.left)
      result.append(self.nucleus)
      result.extend(interfaces.right)
      result.extend(spanners.right)
      result.extend(annotations.right)
      result.extend(self.number_contribution)
      result.extend(client.comments._right)
      return [' '.join(result)]

   @property
   def nucleus(self):
      '''Return string representation of noteheads in self.'''
      nucleus =  [ ]
      # check if we have notehead overrides
      if any([(len(x) or x.style) for x in self._client.noteheads]):
         for notehead in self._client.noteheads:
            nucleus.extend(['\t' + x for x in notehead._formatter._format])
         nucleus = ['\n' + '\n'.join(nucleus) + '\n']
      else:
         for notehead in self._client.noteheads:
            nucleus.extend([x for x in notehead._formatter._format])
      result = '<%s>%s' % (
         ' '.join(nucleus), self._client.duration._product)
      if self._client.tremolo.subdivision:
         result += ' %s' % ''.join(self._client.tremolo.body)
      return result
