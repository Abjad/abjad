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
      client = self._client
      noteheads = client.noteheads
      if any([(len(x) or x.style) for x in noteheads]):
         for notehead in noteheads:
            nucleus.extend(['\t' + x for x in notehead.format.split('\n')])
         nucleus = ['\n' + '\n'.join(nucleus) + '\n']
      else:
         for notehead in noteheads:
            nucleus.extend([x for x in notehead.format.split('\n')])
      result = '<%s>%s' % (
         ' '.join(nucleus), client.duration._product)
      tremolo = client.tremolo
      if tremolo.subdivision:
         result += ' %s' % ''.join(tremolo.body)
      return result
