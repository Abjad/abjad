from abjad.core import _StrictComparator
from abjad.core import LilyPondContextSettingComponentPlugIn
from abjad.core import LilyPondGrobOverrideComponentPlugIn
from abjad.core import LilyPondMiscellaneousCommandComponentPlugIn
from abjad.interfaces import _NavigationInterface
#from abjad.interfaces import _NumberingInterface
from abjad.interfaces import _OffsetInterface
from abjad.interfaces import ParentageInterface


class _Component(_StrictComparator):

   def __init__(self):
      #self.__is_current = False
      #self._is_current = False
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

   def __mul__(self, n):
      from abjad.tools import componenttools
      return componenttools.clone_components_and_remove_all_spanners([self], n)

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
      '''Read-only reference to class-specific duration interface.'''
      return self._duration

   @property
   def format(self):
      '''Read-only version of `self` as LilyPond input code.'''
      self._update_marks_of_entire_score_tree_if_necessary( )
      return self._formatter.format

   @property
   def marks(self):
      '''Read-only reference to ordered list of marks attached to component.
      '''
      return tuple(set(
         self._marks_for_which_component_functions_as_start_component +
         self._marks_for_which_component_functions_as_effective_context))

   @property
   def misc(self):
      '''Read-only reference LilyPond miscellaneous command component plug-in.
      '''
      if not hasattr(self, '_misc'):
         self._misc = LilyPondMiscellaneousCommandComponentPlugIn( )
      return self._misc

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
      attribute_chain = key.split('__')
      most_attributes = attribute_chain[:-1]
      last_attribute = attribute_chain[-1]
      target_object = self
      for attribute in most_attributes:
         target_object = getattr(target_object, attribute)
      setattr(target_object, last_attribute, value)

   ## MANGLED METHODS ##

   def __update_explicit_meters_of_entire_score_tree(self):
      from abjad.tools import componenttools
      from abjad.tools import measuretools
      #print 'updating all explicit meters in score (from %s) ...' % str(self.__class__.__name__)
      total_components_iterated = 0
      score = componenttools.component_to_score_root(self)
      components = componenttools.iterate_components_depth_first(score, 
         capped = True, unique = True, forbid = None, direction = 'left')
      for component in components:
         if isinstance(component, measuretools.DynamicMeasure):
            #print '\tnow updating %s explicit meter ...' % str(component.__class__.__name__)
            component._update_explicit_meter( )
         total_components_iterated += 1
      #print  '... done updating all explicit meters in score (from %s).' % str(
      #   self.__class__.__name__)

   def __update_marks_of_entire_score_tree(self):
      '''Updating marks does not cause prolated offset values to update.
      On the other hand, getting effective mark causes prolated offset values
      to update when at least one mark of appropriate type attaches to score.
      '''
      from abjad.tools import componenttools
      #print 'updating all marks in score (from %s) ...' % str(self.__class__.__name__)
      total_components_iterated = 0
      score = componenttools.component_to_score_root(self)
      components = componenttools.iterate_components_depth_first(score, 
         capped = True, unique = True, forbid = None, direction = 'left')
      for component in components:
         #print '\tnow updating %s marks ...' % str(component.__class__.__name__)
         for mark in component._marks_for_which_component_functions_as_start_component:
            mark._update_effective_context( )
         component._marks_are_current = True
         total_components_iterated += 1
      #print '... done updating all marks in score (from %s).' % str(self.__class__.__name__)
   
   def __update_offset_values_in_seconds_of_entire_score_tree(self):
      from abjad.tools import componenttools
      #print 'updating all offset values in seconds in score ...'
      total_components_iterated = 0
      score = componenttools.component_to_score_root(self)
      components = componenttools.iterate_components_depth_first(score, 
         capped = True, unique = True, forbid = None, direction = 'left')
      for component in components:
         #print '\tnow updating %s offset values in seconds ...' % str(component.__class__.__name__)
         component._offset._update_offset_values_of_component_in_seconds( )
         component._offset_values_in_seconds_are_current = True
         total_components_iterated += 1
      #print 'done updating all offset values in seconds in score.'

   def __update_prolated_offset_values_of_entire_score_tree(self):
      '''Updating prolated offset values does NOT update marks.
      Updating prolated offset values does NOT update offset values in seconds.
      '''
      from abjad.tools import componenttools
      #print 'updating prolated offset values ...',
      total_components_iterated = 0
      score = componenttools.component_to_score_root(self)
      components = componenttools.iterate_components_depth_first(score, 
         capped = True, unique = True, forbid = None, direction = 'left')
      for component in components:
         component._offset._update_prolated_offset_values_of_component( )
         component._prolated_offset_values_are_current = True
         total_components_iterated += 1
      #print total_components_iterated, '... prolated offset values updated.'

   ## PRIVATE UPDATE METHODS ##

   def _mark_entire_score_tree_for_later_update(self, value):
      '''Call immediately AFTER MODIFYING score tree.
      '''
      from abjad.tools import componenttools
      assert value in ('prolated', 'marks', 'seconds')
      for component in componenttools.get_improper_parentage_of_component(self):
         if value == 'prolated':
            component._prolated_offset_values_are_current = False
         elif value == 'marks':
            component._marks_are_current = False
         elif value == 'seconds':
            component._offset_values_of_in_seconds_are_current = False
         else:
            raise ValueError('unknown value: "%s"' % value)

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
      from abjad.tools import componenttools
      #print 'checking marks of entire score tree ...',
      state_flags = self._get_score_tree_state_flags( )
      #print state_flags
      prolated_offset_values, marks, offset_values_in_seconds = state_flags
      if not marks:
         ## updating marks INHERENTLY UPDATES prolated offset values
         self.__update_marks_of_entire_score_tree( )
         self.__update_offset_values_in_seconds_of_entire_score_tree( )
         #print 'update done.'
      else:
         #print 'no need.'
         pass

   def _update_prolated_offset_values_of_entire_score_tree_if_necessary(self):
      #print 'checking prolated offset values of entire score tree ...',
      state_flags = self._get_score_tree_state_flags( )
      prolated_offset_values, marks, offset_values_in_seconds = state_flags
      ## score tree structure change entails prolated offset update
      ## score tree structure change entail dynamic measure meter recalculation
      if not prolated_offset_values:
         self.__update_prolated_offset_values_of_entire_score_tree( )
         self.__update_explicit_meters_of_entire_score_tree( )
      else:
         #print 'no need.'
         pass
