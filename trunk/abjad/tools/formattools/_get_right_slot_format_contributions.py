def _get_right_slot_format_contributions(component):
   '''Ordered list of format-time contributions for right format slot.
   '''
   from abjad.tools.formattools._get_articulation_format_contributions import \
      _get_articulation_format_contributions

   result = [ ]
   result.extend(_get_articulation_format_contributions(component))
   result.sort( )
   return result
