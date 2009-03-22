from abjad.helpers.transfer_all_attributes import _transfer_all_attributes
from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.helpers.leaf_scale import leaf_scale, leaf_scale_binary
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational


def leaf_split(split_dur, leaf):
   assert isinstance(leaf, _Leaf)
   split_dur = Rational(*_duration_token_unpack(split_dur))
   unprolated_split_dur = split_dur / leaf.duration.prolation
   if unprolated_split_dur == 0 or \
      unprolated_split_dur >= leaf.duration.written:
      return [leaf]
   else:
      new_leaf = leaf.copy()
      new_leaf.spanners.clear( )
      _link_new_leaf_to_parent(new_leaf, leaf)
      _update_leaf_spanners(new_leaf, leaf)
      l1 = leaf_scale(unprolated_split_dur, new_leaf)
      l2 = leaf_scale(leaf.duration.written - unprolated_split_dur, leaf)
      return [l1, l2]


def leaf_split_binary(split_dur, leaf):
   assert isinstance(leaf, _Leaf)
   split_dur = Rational(*_duration_token_unpack(split_dur))
   unprolated_split_dur = split_dur / leaf.duration.prolation
   ### TODO: check it unprolated_split_dur is m / 2**n?
   if unprolated_split_dur == 0 or \
      unprolated_split_dur >= leaf.duration.written:
      return [leaf]
   else:
      new_leaf = leaf.copy()
      ### remove afterGrace from new_leaf and Grace from leaf (l2)
      new_leaf.grace.after = None
      leaf.grace.before = None
      ### remove articulations and dynamics
      leaf.articulations = None
      leaf.dynamics = None
      new_leaf.spanners.clear( )
      _link_new_leaf_to_parent(new_leaf, leaf)
      _update_leaf_spanners(new_leaf, leaf)
      l1 = leaf_scale_binary(unprolated_split_dur, new_leaf)
      l2 = leaf_scale_binary(leaf.duration.written-unprolated_split_dur, leaf)
      result = [l1, l2] 
      return result


def _update_leaf_spanners(new_leaf, old_leaf):
#   new_leaf.spanners.clear() 
#   for spanner in old_leaf.spanners.attached:
#      spanner._insert(spanner.index(old_leaf), new_leaf)
   for spanner in old_leaf.spanners.attached:
      if spanner[0] is old_leaf:
         spanner.append_left(new_leaf)

def _link_new_leaf_to_parent(new_leaf, old_leaf):
   parent = old_leaf.parentage.parent
   if parent:
      i = parent.index(old_leaf)              
      parent[i:i] = [new_leaf]
