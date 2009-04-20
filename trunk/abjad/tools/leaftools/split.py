## TODO: leaftools.split( ) completely deprecated. ##
## TODO: Use leaftools.split_general( ) instead.   ##


#from abjad.leaf.leaf import _Leaf
#from abjad.rational.rational import Rational
#from abjad.tools import clone
#from abjad.tools.leaftools.scale import scale
#
#
#def split(leaf, split_dur):
#   assert isinstance(leaf, _Leaf)
#   assert isinstance(split_dur, Rational)
#   leaf_written_duration = leaf.duration.written
#   unprolated_split_dur = split_dur / leaf.duration.prolation
#   if unprolated_split_dur <= 0:
#      return [leaf]
#   if leaf_written_duration <= unprolated_split_dur:
#      return [leaf]
#   new_leaf = clone.unspan([leaf])[0]
#   leaf.splice([new_leaf])
#   new_leaf.grace.before = None
#   new_leaf.articulations = None
#   new_leaf.dynamics.mark = None
#   leaf.grace.after = None
#   l1 = scale(leaf, unprolated_split_dur)
#   l2 = scale(new_leaf, leaf_written_duration - unprolated_split_dur)
#   return [l1, l2]
