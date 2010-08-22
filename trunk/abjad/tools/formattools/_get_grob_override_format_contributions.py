def _get_grob_override_format_contributions(component):
   '''Alphabetized list of LilyPond grob overrides.
   '''
   from abjad.components._Leaf import _Leaf
   from abjad.core.LilyPondGrobProxy import LilyPondGrobProxy
   from abjad.core.LilyPondGrobProxyContextWrapper import LilyPondGrobProxyContextWrapper
   from abjad.tools.lilyfiletools._make_lilypond_override_string import \
      _make_lilypond_override_string
   from abjad.tools.formattools._get_format_contributor_component_interfaces import \
      _get_format_contributor_component_interfaces

   result = [ ]
   for contributor in _get_format_contributor_component_interfaces(component):
      result.extend(getattr(contributor, '_overrides', [ ]))
   if isinstance(component, _Leaf):
      is_once = True
   else:
      is_once = False
   for name, value in vars(component.override).iteritems( ):
      #print name, value
      if isinstance(value, LilyPondGrobProxyContextWrapper):
         context_name, context_wrapper = name.lstrip('_'), value
         #print context_name, context_wrapper
         for grob_name, grob_override_namespace in vars(context_wrapper).iteritems( ):
            #print grob_name, grob_override_namespace
            for grob_attribute, grob_value in vars(grob_override_namespace).iteritems( ):
               #print grob_attribute, grob_value
               result.append(_make_lilypond_override_string(grob_name, grob_attribute, 
                  grob_value, context_name = context_name, is_once = is_once))
      elif isinstance(value, LilyPondGrobProxy):
         grob_name, grob_namespace = name, value
         for grob_attribute, grob_value in vars(grob_namespace).iteritems( ):
            result.append(_make_lilypond_override_string(grob_name, grob_attribute, 
               grob_value, is_once = is_once))
      #print ''
   for override in result[:]:
      if 'NoteHead' in override and 'pitch' in override:
         result.remove(override)
   ## guarantee predictable order of override statements
   result.sort( )
   return result
