from .. leaf.leaf import LeafFormatter
from .. core.interface import _Interface

class ChordFormatter(LeafFormatter):

   def __init__(self, client):
      LeafFormatter.__init__(self, client)

   @property
   def _chordNucleus(self):
      result = '<%s>' % self._client._summary
      if self._client._product:
         result += str(self._client._product)
      if self._client.stem.tremolo:
         result += ' :%s' % self._client.stem.tremolo
      return result

   @property
   def _body(self):
      result = [ ]
      result.extend(self.left)
      if any([len(x) for x in self._client.noteheads]):
         result.append('<')
         for notehead in self._client.noteheads:
            result.extend(['\t' + x for x in notehead._formatter._lily])
         if self._client.stem.tremolo:
            result.append('>%s%s' % 
               (self._client._product, self._client.tremolo.body))
         else:
            result.append('>%s' % self._client._product)
         return ['\n'.join(result)]
      else:
         result.extend(self._collectLocation('_left'))
         result.append(self._chordNucleus)
         result.extend(self._collectLocation('_right'))
         result.extend(self.right)
         result.extend(self._number)
         result.extend(self._client.comments._right)
         return [' '.join(result)]
