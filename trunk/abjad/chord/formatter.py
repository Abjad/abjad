from abjad.core.interface import _Interface
from abjad.leaf.leaf import _LeafFormatter


class _ChordFormatter(_LeafFormatter):

   def __init__(self, client):
      _LeafFormatter.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def _nucleus(self):
      '''String representation of noteheads in chord.
         Return list like all other format-time contributions.'''
      nucleus =  [ ]
      chord = self._client
      noteheads = chord.noteheads
      if any([(len(x) or x.style) for x in noteheads]):
         for notehead in noteheads:
            nucleus.extend(['\t' + x for x in notehead.format.split('\n')])
         nucleus = ['\n' + '\n'.join(nucleus) + '\n']
      else:
         for notehead in noteheads:
            nucleus.extend([x for x in notehead.format.split('\n')])
      result = '<%s>%s' % (
         ' '.join(nucleus), chord.duration._product)
      return [result]
