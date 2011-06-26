from abjad.core import LilyPondContextSettingComponentPlugIn
from abjad.core import LilyPondGrobOverrideComponentPlugIn
from abjad.core import _StrictComparator
from abjad.interfaces import ParentageInterface
from abjad.interfaces import _NavigationInterface
from abjad.interfaces import _OffsetInterface
from abjad.tools import durtools
import copy


class _Component(_StrictComparator):

   __slots__ = ('_duration', '_is_forbidden_to_update', '_marks_are_current', 
      '_marks_for_which_component_functions_as_effective_context',
      '_marks_for_which_component_functions_as_start_component', '_navigator', 
      '_offset', '_offset_values_in_seconds_are_current', '_override', '_parentage', 
      '_prolated_offset_values_are_current', '_set', '_spanners',
      'lily_file', )

   def __init__(self):
      self._is_forbidden_to_update = False
      self._marks_are_current = False
      self._marks_for_which_component_functions_as_effective_context = list( )
      self._marks_for_which_component_functions_as_start_component = list( )
      self._navigator = _NavigationInterface(self)
      self._offset = _OffsetInterface(self)
      self._offset_values_in_seconds_are_current = False
      self._parentage = ParentageInterface(self)
      self._prolated_offset_values_are_current = False
      self._spanners = set([ ])

   ## OVERLOADS ##

   def __copy__(self, *args):
      from abjad.tools import marktools
      from abjad.tools import markuptools
      new = type(self)(*self.__getnewargs__( ))
      if getattr(self, '_override', None) is not None:
         new._override = copy.copy(self.override)
      if getattr(self, '_set', None) is not None:
         new._set = copy.copy(self.set)
      for mark in marktools.get_marks_attached_to_component(self):
         new_mark = copy.copy(mark)
         new_mark.attach_mark(new)
      return new

   def __getnewargs__(self):
      return ( )

   def __mul__(self, n):
      from abjad.tools import componenttools
      return componenttools.copy_components_and_remove_all_spanners([self], n)

   def __rmul__(self, n):
      return self * n

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_pieces(self):
      return self._formatter._format_pieces
   
   @property
   def _ID(self):
      if getattr(self, 'name', None) is not None:
         rhs = self.name
      else:
         rhs = id(self)
      lhs = self.__class__.__name__
      return '%s-%s' % (lhs, rhs)

   ## PUBLIC ATTRIBUTES ##

   @property
   def duration(self):
      '''Read-only duration interface of component.
      '''
      return self._duration

   @property
   def format(self):
      '''Read-only LilyPond input format of component.
      '''
      self._update_marks_of_entire_score_tree_if_necessary( )
      return self._formatter.format

   @property
   def marks(self):
      '''Read-only tuple of marks attached to component.
      '''
      return tuple(set(
         self._marks_for_which_component_functions_as_start_component +
         self._marks_for_which_component_functions_as_effective_context))

   @property
   def override(self):
      '''Read-only reference to LilyPond grob override component plug-in.
      '''
      if not hasattr(self, '_override'):
         self._override = LilyPondGrobOverrideComponentPlugIn( )
      return self._override

   @property
   def set(self):
      '''Read-only reference LilyPond context setting component plug-in.
      '''
      if not hasattr(self, '_set'):
         self._set = LilyPondContextSettingComponentPlugIn( )
      return self._set

   @property
   def spanners(self):
      '''Read-only reference to unordered set of spanners attached to component.
      '''
      return set(self._spanners)
   
   ## PRIVATE METHODS ##

   def _initialize_keyword_values(self, **kwargs):
      for key, value in kwargs.iteritems( ):
         self._set_keyword_value(key, value)

   def _set_keyword_value(self, key, value):
      from fractions import Fraction
      attribute_chain = key.split('__')
      plug_in_name = attribute_chain[0]
      names = attribute_chain[1:]
      if plug_in_name == 'duration':
         attribute_name = names[0]
         command = 'self.%s.%s = %s' % (plug_in_name, attribute_name, repr(value))
         print command
         exec(command)
      elif plug_in_name == 'override':
         if len(names) == 2:
            grob_name, attribute_name = names
            exec('self.override.%s.%s = %s' % (grob_name, attribute_name, repr(value)))
         elif len(names) == 3:
            context_name, grob_name, attribute_name = names
            exec('self.override.%s.%s.%s = %s' % (
               context_name, grob_name, attribute_name, repr(value)))
         else:
            raise ValueError
      elif plug_in_name == 'set':
         if len(names) == 1:
            setting_name = names[0]
            exec('self.set.%s = %s' % (setting_name, repr(value)))
         elif len(names) == 2:
            context_name, setting_name = names
            exec('self.set.%s.%s = %s' % (context_name, setting_name, repr(value)))
         else:
            raise ValueError
      else:
         raise ValueError('\n\t: Unknown keyword argument plug-in name: "%s".' % plug_in_name)

   ## MANGLED METHODS ##

   def __update_marks_of_entire_score_tree(self):
      '''Updating marks does not cause prolated offset values to update.
      On the other hand, getting effective mark causes prolated offset values
      to update when at least one mark of appropriate type attaches to score.
      '''
      from abjad.tools import componenttools
      score_root = componenttools.component_to_score_root(self)
      components = componenttools.iterate_components_depth_first(score_root, 
         capped = True, unique = True, forbid = None, direction = 'left')
      for component in components:
         for mark in component._marks_for_which_component_functions_as_start_component:
            if hasattr(mark, '_update_effective_context'):
               mark._update_effective_context( )
         component._marks_are_current = True
   
   def __update_offset_values_in_seconds_of_entire_score_tree(self):
      from abjad.tools import componenttools
      score_root = componenttools.component_to_score_root(self)
      components = componenttools.iterate_components_depth_first(score_root, 
         capped = True, unique = True, forbid = None, direction = 'left')
      for component in components:
         component._offset._update_offset_values_of_component_in_seconds( )
         component._offset_values_in_seconds_are_current = True

   def __update_prolated_offset_values_of_entire_score_tree(self):
      '''Updating prolated offset values does NOT update marks.
      Updating prolated offset values does NOT update offset values in seconds.
      '''
      from abjad.tools import componenttools
      score_root = componenttools.component_to_score_root(self)
      components = componenttools.iterate_components_depth_first(score_root, 
         capped = True, unique = True, forbid = None, direction = 'left')
      for component in components:
         component._offset._update_prolated_offset_values_of_component( )
         component._prolated_offset_values_are_current = True

   ## PRIVATE UPDATE METHODS ##

   def _allow_component_update(self):
      self._is_forbidden_to_update = False

   def _mark_entire_score_tree_for_later_update(self, value):
      '''Call immediately AFTER MODIFYING score tree.
      Only dynamic measures mark time signature for udpate.
      '''
      from abjad.tools import componenttools
      assert value in ('prolated', 'marks', 'seconds')
      for component in componenttools.get_improper_parentage_of_component(self):
         if value == 'prolated':
            component._prolated_offset_values_are_current = False
         elif value == 'marks':
            component._marks_are_current = False
         elif value == 'seconds':
            component._offset_values_in_seconds_are_current = False
         else:
            raise ValueError('unknown value: "%s"' % value)
         if hasattr(component, '_time_signature_is_current'):
            component._time_signature_is_current = False

   def _forbid_component_update(self):
      self._is_forbidden_to_update = True

   def _get_score_tree_state_flags(self):
      from abjad.tools import componenttools
      prolated_offset_values_are_current = True
      marks_are_current = True
      offset_values_in_seconds_are_current = True
      for component in componenttools.get_improper_parentage_of_component(self):
         if prolated_offset_values_are_current:
            if not component._prolated_offset_values_are_current:
               prolated_offset_values_are_current = False
         if marks_are_current:
            if not component._marks_are_current:
               marks_are_current = False
         if offset_values_in_seconds_are_current:
            if not component._offset_values_in_seconds_are_current:
               offset_values_in_seconds_are_current = False
      return (prolated_offset_values_are_current, marks_are_current,
         offset_values_in_seconds_are_current)

   def _update_marks_of_entire_score_tree_if_necessary(self):
      '''Call immediately BEFORE READING effective mark.
      '''
      if self._is_forbidden_to_update:
         return
      state_flags = self._get_score_tree_state_flags( )
      marks_are_current = state_flags[1]
      if not marks_are_current:
         self.__update_marks_of_entire_score_tree( )
         self.__update_offset_values_in_seconds_of_entire_score_tree( )

   def _update_prolated_offset_values_of_entire_score_tree_if_necessary(self):
      if self._is_forbidden_to_update:
         return
      state_flags = self._get_score_tree_state_flags( )
      prolated_offset_values_are_current = state_flags[0]
      if not prolated_offset_values_are_current:
         self.__update_prolated_offset_values_of_entire_score_tree( )
