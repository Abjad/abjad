from abjad.interfaces._Interface import _Interface


class InterfaceAggregator(_Interface):
   '''Aggregate information about all format-contributing interfaces.'''

   def __init__(self, client):
      '''Bind to client. Note that private contributors list is not
      populate in this class. Rather, each class inheriting from format
      contributor is reponsible for registering itself and adding
      its class to the private contributors list initialized here.'''
      _Interface.__init__(self, client)
      self._contributors = [ ]
      self._contributors_sorted = False

   ## PUBLIC ATTRIBUTES ##

   @property
   def after(self):
      '''Ordered list of format-time contributions for after format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_after', [ ]))
      result.extend(self._client.misc._get_formatted_commands_for_target_slot('after'))
      result.sort( )
      return result

   @property
   def before(self):
      '''Ordered list of format-time contributions for before format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_before', [ ]))
      result.extend(self._client.misc._get_formatted_commands_for_target_slot('before'))
      result.sort( )
      return result

   @property
   def closing(self):
      '''Ordered list of format-time contributions for closing format slot.'''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_closing', [ ]))
      result.extend(self._client.misc._get_formatted_commands_for_target_slot('closing'))
      result.sort( )
      return result

   @property
   def contributors(self):
      from abjad.components.Chord import Chord
      from abjad.tools.notetools.NoteHead import NoteHead
      if not self._contributors_sorted:
         self._contributors.sort(lambda x, y:
            cmp(x.__class__.__name__, y.__class__.__name__))
         self._contributors_sorted = True
      ## TODO: Remove client-testing hack. ##
      if isinstance(self._client, Chord):
         note_head = [x for x in self._contributors if isinstance(x, NoteHead)]
         if note_head:
            note_head = note_head[0]
            self._contributors.remove(note_head) 
      return self._contributors

   @property
   def contributions(self):
      '''Returns an ordered list of contribution triples.'''
      result = [ ]
      locations = ('before', 'overrides', 'opening', 'left', 
         'right', 'closing', 'reverts', 'after')
      for contributor in self.contributors:
         for location in locations:
            contributions = getattr(contributor, location, None)
            if contributions:
               result.append(((contributor, location), contributions))
      return result
   
   @property
   def left(self):
      '''Ordered list of format-time contributions for left format slot.
      '''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_left', [ ]))
      result.extend(self._client.misc._get_formatted_commands_for_target_slot('left'))
      result.sort( )
      return result

   @property
   def opening(self):
      '''Ordered list of format-time contributions for opening format slot.
      '''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_opening', [ ]))
      result.extend(self._client.misc._get_formatted_commands_for_target_slot('opening'))
      result.sort( )
      return result

   @property
   def overrides(self):
      '''Alphabetized list of LilyPond grob overrides.
      '''
      from abjad.components._Leaf import _Leaf
      from abjad.core.LilyPondGrobProxy import LilyPondGrobProxy
      from abjad.core.LilyPondGrobProxyContextWrapper import LilyPondGrobProxyContextWrapper
      from abjad.tools.lilyfiletools._make_lilypond_override_string import \
         _make_lilypond_override_string
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_overrides', [ ]))
      if isinstance(self._client, _Leaf):
         is_once = True
      else:
         is_once = False
      for name, value in vars(self._client.override).iteritems( ):
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

   @property
   def reverts(self):
      '''Alphabetized list of LilyPond grob reverts.
      '''
      from abjad.components._Leaf import _Leaf
      from abjad.core.LilyPondGrobProxy import LilyPondGrobProxy
      from abjad.core.LilyPondGrobProxyContextWrapper import LilyPondGrobProxyContextWrapper
      from abjad.tools.lilyfiletools._make_lilypond_revert_string import \
         _make_lilypond_revert_string
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_reverts', [ ]))
      if not isinstance(self._client, _Leaf):
         for name, value in vars(self._client.override).iteritems( ):
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

   @property
   def right(self):
      '''Ordered list of format-time contributions for right format slot.
      '''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, '_right', [ ]))
      result.extend(self._client.misc._get_formatted_commands_for_target_slot('right'))
      result.sort( )
      return result

   @property
   def settings(self):
      '''Ordered data structure of format-time context settings.
      '''
      result = [ ]
      for contributor in self.contributors:
         result.extend(getattr(contributor, 'settings', [ ]))
      from abjad.components._Leaf import _Leaf
      from abjad.components._Measure import _Measure
      from abjad.tools.lilyfiletools._format_lilypond_context_setting_inline import \
         _format_lilypond_context_setting_inline
      from abjad.tools.lilyfiletools._format_lilypond_context_setting_in_with_block import \
         _format_lilypond_context_setting_in_with_block
      if isinstance(self._client, (_Leaf, _Measure)):
         for name, value in vars(self._client.set).iteritems( ):
            ## if we've found a leaf LilyPondContextNamespace
            if name.startswith('_'):
               ## parse all the public names in the LilyPondContextNamespace
               for x, y in vars(value).iteritems( ):
                  if not x.startswith('_'):
                     result.append(_format_lilypond_context_setting_inline(x, y, name))
            ## otherwise we've found a default leaf context setting
            else:
               ## parse default context setting
               result.append(_format_lilypond_context_setting_inline(name, value))
      else:
         for name, value in vars(self._client.set).iteritems( ):
            result.append(_format_lilypond_context_setting_in_with_block(name, value))
      result.sort( )
      return result

   ## PUBLIC METHODS ##

   def report(self, output = 'screen'):
      '''Deliver report of format-time contributions.
      Order by interface, location, contribution.
      '''
      result = ''
      for ((contributor, location), contributions) in self.contributions:
         result += '%s\n' % contributor.__class__.__name__
         result += '\t%s\n' % location
         for contribution in contributions:
            result += '\t\t%s\n' % contribution
      if output == 'screen':
         print result
      else:
         return result
