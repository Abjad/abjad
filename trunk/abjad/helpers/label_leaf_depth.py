from abjad.tools import iterate


def label_leaf_depth(expr):
   '''Iterate expr and label depth of every leaf.'''

   from abjad.leaf.leaf import _Leaf
   for leaf in iterate.naive(expr, _Leaf):
      label = r'\small %s' % leaf.parentage.depth
      leaf.markup.down.append(label)
