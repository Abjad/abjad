from abjad.tools import iterate


def leaf_depth_tuplet(expr):
   '''Iterate `expr` and label tuplet depth of every leaf.'''

   from abjad.leaf.leaf import _Leaf
   for leaf in iterate.naive(expr, _Leaf):
      label = r'\small %s' % leaf.parentage.depth_tuplet
      leaf.markup.down.append(label)
