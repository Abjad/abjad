from abjad.interfaces._Interface import _Interface
from abjad.components._Leaf._LeafFormatter import _LeafFormatter


class _ChordFormatter(_LeafFormatter):

   def __init__(self, client):
      _LeafFormatter.__init__(self, client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _nucleus(self):
      '''String representation of note_heads in chord.
      Return list like all other format-time contributions.
      '''
      result =  [ ]
      chord = self.leaf
      note_heads = chord.note_heads
      if any(['\n' in x.format for x in note_heads]):
         #print 'overrides!'
         for note_head in note_heads:
            format = note_head.format
            format_list = format.split('\n')
            format_list = ['\t' + x for x in format_list]
            result.extend(format_list)
         result.insert(0, '<')
         result.append('>')
         result = '\n'.join(result)
         result += str(chord.duration)
      else:
         #print 'no overrides'
         result.extend([x.format for x in note_heads])
         result = '<%s>%s' % (
            ' '.join(result), chord.duration)
      ## single string, but wrapped in list bc contribution
      return [result]
