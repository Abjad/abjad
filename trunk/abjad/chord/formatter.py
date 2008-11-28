from abjad.core.interface import _Interface
from abjad.leaf.leaf import _LeafFormatter


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
