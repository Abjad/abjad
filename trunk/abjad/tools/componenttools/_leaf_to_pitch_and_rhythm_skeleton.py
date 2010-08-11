from abjad.components.Chord import Chord
from abjad.components.Note import Note
from abjad.tools.componenttools._get_leaf_keyword_attributes import _get_leaf_keyword_attributes


def _leaf_to_pitch_and_rhythm_skeleton(leaf, include_keyword_attributes = False):
   class_name = leaf.__class__.__name__
   duration = repr(leaf.duration.written)
   if include_keyword_attributes:
      keyword_attributes = _get_leaf_keyword_attributes(leaf)
   else:
      keyword_attributes = [ ]
   keyword_attributes = ['\t' + x for x in keyword_attributes]
   if keyword_attributes:
      keyword_attributes = ',\n'.join(keyword_attributes)
      keyword_attributes = '\n' + keyword_attributes
      keyword_attributes = [keyword_attributes]
   if isinstance(leaf, Note):
      arguments = [leaf.pitch.pair, duration]
   elif isinstance(leaf, Chord):
      arguments = [leaf.pairs, duration]
   else:
      arguments = [duration]
   arguments = [str(x) for x in arguments]
   arguments.extend(keyword_attributes)
   arguments = ', '.join(arguments)
   return '%s(%s)' % (class_name, arguments)
