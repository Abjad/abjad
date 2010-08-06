from abjad.tools import iterate


def _label_leaves_in_expr_with_leaf_durations(expr, 
   show = ['written', 'prolated'], ties = 'together'):
   r'''Label leaves in expr with written leaf duration, prolated leaf duration
   or both written and prolated leaf durations.

   .. versionchanged:: 1.1.2
      renamed ``label.leaf_durations( )`` to
      ``leaftools.label_leaves_in_expr_with_leaf_duration( )``.
   '''
   
   for leaf in iterate.leaves_forward_in_expr(expr):
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
         elif leaf.tie.spanner._is_my_first_leaf(leaf):
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
