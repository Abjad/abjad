from abjad.helpers.iterate import iterate


def label_leaf_depth(expr):
   '''Iterate expr and label depth of every leaf.'''

   for leaf in iterate(expr, '_Leaf'):
      label = r'\small %s' % leaf.parentage.depth
      leaf.markup.down.append(label)
