from abjad.interfaces.interface.interface import _Interface
from abjad.leaf.leaf import _LeafFormatter


class _ChordFormatter(_LeafFormatter):

   def __init__(self, client):
      _LeafFormatter.__init__(self, client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _nucleus(self):
      '''String representation of noteheads in chord.
         Return list like all other format-time contributions.
         .. todo:: return immutable tuple of contributions.'''
      result =  [ ]
      chord = self.leaf
      noteheads = chord.noteheads
#      if any([(len(x) or x.style) for x in noteheads]):
#         for notehead in noteheads:
#            result.extend(['\t' + x for x in notehead.format.split('\n')])
#         result = ['\n' + '\n'.join(result) + '\n']
#      else:
#         for notehead in noteheads:
#            result.extend([x for x in notehead.format.split('\n')])
      if any(['\n' in x.format for x in noteheads]):
         #print 'overrides!'
         for notehead in noteheads:
            format = notehead.format
            format_list = format.split('\n')
            format_list = ['\t' + x for x in format_list]
            result.extend(format_list)
         result.insert(0, '<')
         result.append('>')
         result = '\n'.join(result)
         result += str(chord.duration._product)
      else:
         #print 'no overrides'
         result.extend([x.format for x in noteheads])
         result = '<%s>%s' % (
            ' '.join(result), chord.duration._product)
      ## single string, but wrapped in list bc contribution
      return [result]
