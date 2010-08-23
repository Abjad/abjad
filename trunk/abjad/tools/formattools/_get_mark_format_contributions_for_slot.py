from abjad.components._Leaf import _Leaf


def _get_mark_format_contributions_for_slot(leaf, slot):

   result = [ ]
   if not isinstance(leaf, _Leaf):
      return result
   marks = set([ ])
   for component in leaf.parentage.improper_parentage:
      for mark in component.marks:
         if mark._format_slot == slot:
            if mark.start_component.offset.start == leaf.offset.start:
               marks.add(mark)
   for mark in marks:
      mark_format = mark.format
      if isinstance(mark_format, (tuple, list)):
         result.extend(mark_format)
      else:
         result.append(mark_format)
   result.sort( )
   return result   
