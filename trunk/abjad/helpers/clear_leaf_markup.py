from abjad.helpers.iterate import iterate


def clear_leaf_markup(expr):
   '''Empty t.markup.up and t.markup.down for all leaves in expr.'''

   for leaf in iterate(expr, '_Leaf'):
      leaf.markup.up = [ ]
      leaf.markup.down = [ ]   
