def _get_grob_revert_format_contributions(component):
   '''Alphabetized list of LilyPond grob reverts.
   '''
   from abjad.components._Leaf import _Leaf
   from abjad.core.LilyPondGrobProxy import LilyPondGrobProxy
   from abjad.core.LilyPondGrobProxyContextWrapper import LilyPondGrobProxyContextWrapper
   from abjad.tools.lilyfiletools._make_lilypond_revert_string import \
      _make_lilypond_revert_string

   result = [ ]
   if not isinstance(component, _Leaf):
      for name, value in vars(component.override).iteritems( ):
         #print name, value
         if isinstance(value, LilyPondGrobProxyContextWrapper):
            context_name, context_wrapper = name.lstrip('_'), value
            #print context_name, context_wrapper
            for grob_name, grob_override_namespace in vars(context_wrapper).iteritems( ):
               #print grob_name, grob_override_namespace
               for grob_attribute, grob_value in vars(grob_override_namespace).iteritems( ):
                  #print grob_attribute, grob_value
                  result.append(_make_lilypond_revert_string(
                     grob_name, grob_attribute, context_name = context_name))
         elif isinstance(value, LilyPondGrobProxy):
            grob_name, grob_namespace = name, value
            for grob_attribute, grob_value in vars(grob_namespace).iteritems( ):
               result.append(_make_lilypond_revert_string(grob_name, grob_attribute))
   ## guarantee predictable order of revert statements
   result.sort( )
   return result
