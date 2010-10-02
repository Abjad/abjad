def _get_grob_revert_format_contributions(component):
   '''Alphabetized list of LilyPond grob reverts.
   '''
   from abjad.components._Leaf import _Leaf

   result = [ ]
   if not isinstance(component, _Leaf):
      result.extend(component.override._list_format_contributions('revert'))
   return result
