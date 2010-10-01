def _get_left_slot_format_contributions(component):
   '''Ordered list of format-time contributions for left format slot.
   '''
   from abjad.tools.formattools._get_format_contributor_component_interfaces import \
      _get_format_contributor_component_interfaces

   result = [ ]
   for contributor in _get_format_contributor_component_interfaces(component):
      result.extend(getattr(contributor, '_left', [ ]))
   #result.extend(component.misc._get_formatted_commands_for_target_slot('left'))
   result.sort( )
   return result
