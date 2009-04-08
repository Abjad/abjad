from abjad.tools import iterate


def label_leaf_layer(expr):
   '''Iterate expr and label layer of every leaf.'''

   from abjad.leaf.leaf import _Leaf
   for leaf in iterate.naive(expr, _Leaf):
      label = r'\small %s' % leaf.parentage.layer
      leaf.markup.down.append(label)
