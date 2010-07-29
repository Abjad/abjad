from abjad.tools import iterate


def expr_has_leaf_with_dotted_written_duration(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` has at least one leaf with a dotted writtern duration::

      abjad> notes = leaftools.make_notes([0], [(1, 16), (2, 16), (3, 16)])
      abjad> leaftools.expr_has_leaf_with_dotted_written_duration(notes)
      True
   
   False otherwise::

      abjad> notes = leaftools.make_notes([0], [(1, 16), (2, 16), (4, 16)])
      abjad> leaftools.expr_has_leaf_with_dotted_written_duration(notes)
      False

   .. versionchanged:: 1.1.2
      renamed ``leaftools.has_leaf_with_dotted_written_duration_in( )`` to
      ``leaftools.expr_has_leaf_with_dotted_written_duration( )``.
   '''

   for leaf in iterate.leaves_forward_in_expr(expr):
      if not leaf.duration.written._numerator == 1:
         return True
   return False
