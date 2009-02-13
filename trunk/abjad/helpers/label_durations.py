from abjad.helpers.iterate import iterate


def label_leaf_durations(expr, show = ['written', 'prolated']):
   '''Iterate expr and label all written and prolated durations.'''
   
   for leaf in iterate(expr, '_Leaf'):
      if leaf.duration.multiplier is not None:
         multiplier = '* %s' % str(leaf.duration.multiplier)
      else:
         multiplier = ''
      if 'written' in show:
         label = r'\small %s%s' % (leaf.duration.written, multiplier)
         leaf.markup.down.append(label)
      if 'prolated' in show:
         leaf.markup.down.append(r'\small %s' % leaf.duration.prolated)
