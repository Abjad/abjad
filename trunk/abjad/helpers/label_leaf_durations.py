from abjad.tools import iterate


def label_leaf_durations(expr, 
   show = ['written', 'prolated'], ties = 'together'):
   '''Iterate expr and label all written and prolated durations.'''
   
   from abjad.leaf.leaf import _Leaf
   for leaf in iterate.naive(expr, _Leaf):
      if ties == 'together':
         if not leaf.tie.spanned:
            if leaf.duration.multiplier is not None:
               multiplier = '* %s' % str(leaf.duration.multiplier)
            else:
               multiplier = ''
            if 'written' in show:
               label = r'\small %s%s' % (leaf.duration.written, multiplier)
               leaf.markup.down.append(label)
            if 'prolated' in show:
               leaf.markup.down.append(r'\small %s' % leaf.duration.prolated)
         elif leaf.tie.spanner._isMyFirstLeaf(leaf):
            tie = leaf.tie.spanner
            if 'written' in show:
               written = sum([x.duration.written for x in tie])
               label = r'\small %s' % written
               leaf.markup.down.append(label)
            if 'prolated' in show:
               prolated = sum([x.duration.prolated for x in tie])
               label = r'\small %s' % prolated
               leaf.markup.down.append(label)
      else:
         raise ValueError('unknown value for tie treatment.')
