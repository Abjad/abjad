#def _get_format_contributor_component_interfaces(component):
#   '''Format helper.
#   '''
#
#   ## all possible format contributor interfaces for any component;
#   ## this is a temporary solution because this list must be updated by hand
#   format_contributor_interface_names = (
#      'articulations',
#      'breaks',
#      'clef',
#      'key_signature',
#      'markup',
#      'meter',
#      'staff',
#      'tempo',
#      )
#
#   ## find format contributor interfaces currently bound to component
#   result = [ ]
#   for format_contributor_interface_name in format_contributor_interface_names:
#      format_contributor_interface = getattr(component, format_contributor_interface_name, None)
#      if hasattr(component, '_' + format_contributor_interface_name):
#         format_contributor_interface = getattr(component, format_contributor_interface_name)
#         result.append(format_contributor_interface)
#   result.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
#   print 'DEBUG: %s' % result
#   if result:
#      raise SystemExit
#   return result
