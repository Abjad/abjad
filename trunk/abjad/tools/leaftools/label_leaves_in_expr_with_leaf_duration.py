from abjad.tools import iterate


def label_leaves_in_expr_with_leaf_duration(expr, 
   show = ['written', 'prolated'], ties = 'together'):
   r'''Label the duration of every leaf in `expr`.

   When ``show = ['written']`` label only the written duration of
   leaves in `expr`. ::

      abjad> tuplet = FixedDurationTuplet((1, 4), macros.scale(3))
      abjad> leaftools.label_leaves_in_expr_with_leaf_duration(tuplet, show = ['written'])
      abjad> f(tuplet)
      \times 2/3 {
              c'8 _ \markup { \small 1/8 }
              d'8 _ \markup { \small 1/8 }
              e'8 _ \markup { \small 1/8 }
      }

   When ``show = ['prolated']`` label only the prolated duration of leaves
   in `expr`. ::

      abjad> tuplet = FixedDurationTuplet((1, 4), macros.scale(3))
      abjad> leaftools.label_leaves_in_expr_with_leaf_duration(tuplet, show = ['prolated'])
      abjad> f(tuplet)
      \times 2/3 {
              c'8 _ \markup { \small 1/12 }
              d'8 _ \markup { \small 1/12 }
              e'8 _ \markup { \small 1/12 }
      }

   When ``show = ['written', 'prolated']`` label both the written and
   prolated duration of leaves in `expr`. ::

      abjad> tuplet = FixedDurationTuplet((1, 4), macros.scale(3))
      abjad> leaftools.label_leaves_in_expr_with_leaf_duration(tuplet)
      abjad> f(tuplet)
      \times 2/3 {
              c'8 _ \markup { \column { \small 1/8 \small 1/12 } }
              d'8 _ \markup { \column { \small 1/8 \small 1/12 } }
              e'8 _ \markup { \column { \small 1/8 \small 1/12 } }
      }

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
