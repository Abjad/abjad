from abjad.core.interface import _Interface
from abjad.leaf.leaf import _LeafFormatter


class _ChordFormatter(_LeafFormatter):

   def __init__(self, client):
      _LeafFormatter.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def nucleus(self):
      '''String representation of noteheads in chord.
         Return list like all other format-time contributions.'''
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
      return [result]
