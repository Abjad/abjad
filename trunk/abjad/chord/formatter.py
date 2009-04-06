from abjad.core.interface import _Interface
from abjad.leaf.leaf import _LeafFormatter


class _ChordFormatter(_LeafFormatter):

   def __init__(self, client):
      _LeafFormatter.__init__(self, client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _nucleus(self):
      '''String representation of noteheads in chord.
         Return list like all other format-time contributions.'''
      result =  [ ]
      chord = self.leaf
      noteheads = chord.noteheads
      if any([(len(x) or x.style) for x in noteheads]):
         for notehead in noteheads:
            result.extend(['\t' + x for x in notehead.format.split('\n')])
         result = ['\n' + '\n'.join(result) + '\n']
      else:
         for notehead in noteheads:
            result.extend([x for x in notehead.format.split('\n')])
      result = '<%s>%s' % (
         ' '.join(result), chord.duration._product)
      return [result]
