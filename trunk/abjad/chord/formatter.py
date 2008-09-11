from abjad.leaf.leaf import _LeafFormatter
from abjad.core.interface import _Interface

class _ChordFormatter(_LeafFormatter):

   def __init__(self, client):
      _LeafFormatter.__init__(self, client)

   @property
   def _chordNucleus(self):
      nucleus =  [ ]
      # check if we have notehead overrides
      if any([(len(x) or x.style) for x in self._client.noteheads]):
         for notehead in self._client.noteheads:
            nucleus.extend(['\t' + x for x in notehead._formatter._lily])
         nucleus = ['\n' + '\n'.join(nucleus) + '\n']
      else:
         for notehead in self._client.noteheads:
            nucleus.extend([x for x in notehead._formatter._lily])
      result = '<%s>%s' % (
         ' '.join(nucleus), self._client.duration._product)
      if self._client.tremolo.subdivision:
         result += ' %s' % ''.join(self._client.tremolo.body)
      return result

   @property
   def _body(self):
      result = [ ]
      result.extend(self.left)
      result.extend(self._collectLocation('_left'))
      result.append(self._chordNucleus)
      result.extend(self._collectLocation('_right'))
      result.extend(self.right)
      result.extend(self._number)
      result.extend(self._client.comments._right)
      return [' '.join(result)]


#   @property
#   def _chordNucleus(self):
#      result = '<%s>%s' % (
#         self._client._summary, self._client.duration._product)
#      if self._client.stem.tremolo:
#         result += ' :%s' % self._client.stem.tremolo
#      return result
#
#   @property
#   def _body(self):
#      result = [ ]
#      result.extend(self.left)
#      if any([len(x) for x in self._client.noteheads]):
#         result.append(' '.join(self._collectLocation('_left') + ['<']))
#         for notehead in self._client.noteheads:
#            result.extend(['\t' + x for x in notehead._formatter._lily])
#         if self._client.stem.tremolo:
#            result.append('>%s%s' % 
#               (self._client.duration._product, self._client.tremolo.body))
#         else:
#            closing = ['>%s' % self._client.duration._product]
#            closing += self._collectLocation('_right')
#            result.append(' '.join(closing))
#         return ['\n'.join(result)]
#      else:
#         result.extend(self._collectLocation('_left'))
#         result.append(self._chordNucleus)
#         result.extend(self._collectLocation('_right'))
#         result.extend(self.right)
#         result.extend(self._number)
#         result.extend(self._client.comments._right)
#         return [' '.join(result)]
