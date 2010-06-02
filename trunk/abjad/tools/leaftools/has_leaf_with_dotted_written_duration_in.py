from abjad.tools import iterate


def has_leaf_with_dotted_written_duration_in(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` has at least one leaf with a dotted writtern duration::

      abjad> notes = construct.notes([0], [(1, 16), (2, 16), (3, 16)])
      abjad> leaftools.has_leaf_with_dotted_written_duration_in(notes)
      True
   
   False otherwise::

      abjad> notes = construct.notes([0], [(1, 16), (2, 16), (4, 16)])
      abjad> leaftools.has_leaf_with_dotted_written_duration_in(notes)
      False
   '''

   for leaf in iterate.leaves_forward_in(expr):
      if not leaf.duration.written._numerator == 1:
         return True
   return False
