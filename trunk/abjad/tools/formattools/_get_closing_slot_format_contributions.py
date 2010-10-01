def _get_closing_slot_format_contributions(component):
   '''Ordered list of format-time contributions for closing format slot.
   '''
#   from abjad.tools.formattools._get_format_contributor_component_interfaces import \
#      _get_format_contributor_component_interfaces

   result = [ ]
#   for contributor in _get_format_contributor_component_interfaces(component):
#      result.extend(getattr(contributor, '_closing', [ ]))
   result.sort( )
   return result
