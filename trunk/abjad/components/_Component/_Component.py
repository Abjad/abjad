from abjad.core import _StrictComparator
from abjad.core import LilyPondContextSettingComponentPlugIn
from abjad.core import LilyPondGrobOverrideComponentPlugIn
from abjad.core import LilyPondMiscellaneousCommandComponentPlugIn
from abjad.interfaces import _NavigationInterface
from abjad.interfaces import BreaksInterface
from abjad.interfaces import CommentsInterface
from abjad.interfaces import ClefInterface
from abjad.interfaces import DirectivesInterface
from abjad.interfaces import HistoryInterface
from abjad.interfaces import MeterInterface
#from abjad.interfaces import NumberingInterface
from abjad.interfaces import OffsetInterface
from abjad.interfaces import ParentageInterface
from abjad.interfaces import StaffInterface
#from abjad.interfaces import TempoInterface


class _Component(_StrictComparator):

   def __init__(self):
      #self.__is_current = False
      self._marks_are_current = False
      self._offset_values_in_seconds_are_current = False
      self._prolated_offset_values_are_current = False
      #self._is_current = False
      self._lily_file = None
      self._marks_for_which_component_functions_as_effective_context = list( )
      self._marks_for_which_component_functions_as_start_component = list( )
      self._name = None
      self._navigator = _NavigationInterface(self)
      self._offset = OffsetInterface(self)
      self._parentage = ParentageInterface(self)
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
      if self.name is not None:
         rhs = self.name
      else:
         rhs = id(self)
      lhs = self.__class__.__name__
      return '%s-%s' % (lhs, rhs)

   ## PUBLIC ATTRIBUTES ##

   @property
   def breaks(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.breaks.interface.BreaksInterface`.'''
      if not hasattr(self, '_breaks'):
         self._breaks = BreaksInterface(self)
      return self._breaks

   @property
   def clef(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.clef.interface.ClefInterface`.'''
      if not hasattr(self, '_clef'):
         self._clef = ClefInterface(self)
      return self._clef

   @property
   def comments(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.comments.interface.CommentsInterface`.'''
      if not hasattr(self, '_comments'):
         self._comments = CommentsInterface( )
      return self._comments

   @property
   def directives(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.directives.interface.DirectivesInterface`.'''
      if not hasattr(self, '_directives'):
         self._directives = DirectivesInterface(self)
      return self._directives

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
   def history(self):
      '''Read-only reference to 
      :class:`~abjad.interfaces.history.interface.HistoryInterface`.'''
      if not hasattr(self, '_history'):
         self._history = HistoryInterface(self)
      return self._history

   @property
   def leaves(self):
      '''Read-only tuple of all leaves in `self`.

      .. versionchanged:: 1.1.1'''
      from abjad.tools import leaftools
      return tuple(leaftools.iterate_leaves_forward_in_expr(self))

   @property
   def lily_file(self):
      '''.. versionadded:: 1.1.2
      Read-only reference to .ly file in which 
      component is housed, if any.'''
      return self._lily_file

   @property
   def marks(self):
      '''Read-only reference to ordered list of marks attached to component.
      '''
      return tuple(set(
         self._marks_for_which_component_functions_as_start_component +
         self._marks_for_which_component_functions_as_effective_context))

   @property
   def meter(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.meter.interface.MeterInterface`.''' 
      if not hasattr(self, '_meter'):
         self._meter = MeterInterface(self)
      return self._meter

   @property
   def misc(self):
      '''Read-only reference LilyPond miscellaneous command component plug-in.
      '''
      if not hasattr(self, '_misc'):
         self._misc = LilyPondMiscellaneousCommandComponentPlugIn( )
      return self._misc

   @property
   def music(self):
      '''Read-only tuple of music in `self`.'''
      if hasattr(self, '_music'):
         return tuple(self._music)
      else:
         return tuple( )

   @apply
   def name( ):
      def fget(self):
         '''Read-write name of component. Must be string or none.'''
         return self._name
      def fset(self, arg):
         assert isinstance(arg, (str, type(None)))
         self._name = arg
      return property(**locals( ))

   @property
   def offset(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.offset.interface.OffsetInterface`.'''
      return self._offset

   @property
   def override(self):
      '''Read-only reference to LilyPond grob override component plug-in.
      '''
      if not hasattr(self, '_override'):
         self._override = LilyPondGrobOverrideComponentPlugIn( )
      return self._override

   @property
   def parentage(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.parentage.interface.ParentageInterface`.'''
      return self._parentage

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
   
   @property
   def staff(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.staff.interface.StaffInterface`.'''
      if not hasattr(self, '_staff'):
         #self._staff = StaffInterface(self, self._update)
         self._staff = StaffInterface(self)
      return self._staff

#   @property
#   def tempo(self):
#      '''Read-only reference to
#      :class:`~abjad.interfaces.tempo.interface.TempoInterface`.'''
#      if not hasattr(self, '_tempo'):
#         self._tempo = TempoInterface(self)
#      return self._tempo

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

   ## PUBLIC METHODS ##

   def extend_in_parent(self, components):
      r'''.. versionadded:: 1.1.1

      Extend `components` rightwards of `self` in parent.

      Do not extend edge spanners. ::

         abjad> t = Voice(macros.scale(3))
         abjad> spannertools.BeamSpanner(t[:])
         abjad> t[-1].extend_in_parent(macros.scale(3))

      ::

         abjad> print t.format
         \new Voice {
            c'8 [
            d'8
            e'8 ]
            c'8
            d'8
            e'8
         }
      '''

      from abjad.tools import componenttools
      from abjad.tools import componenttools
      assert componenttools.all_are_components(components)
      parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([self])
      if parent is not None:
         after = stop + 1
         parent[after:after] = components
      return [self] + components

   def extend_left_in_parent(self, components):
      r'''.. versionadded:: 1.1.1

      Extend `components` leftwards of `self` in parent.

      Do not extend edge spanners. ::

         abjad> t = Voice(macros.scale(3))
         abjad> spannertools.BeamSpanner(t[:])
         abjad> t[0].extend_in_parent(macros.scale(3))

      ::

         abjad> print t.format
         \new Voice {
            c'8 
            d'8
            e'8 
            c'8 [
            d'8
            e'8 ]
         }
      '''

      from abjad.tools import componenttools
      from abjad.tools import componenttools
      assert componenttools.all_are_components(components)
      parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([self])
      if parent is not None:
         parent[start:start] = components
      return components + [self] 

   def splice(self, components):
      '''Splice `components` after `self`.
      Extend spanners rightwards to attach to all components in list.'''
      from abjad.tools import componenttools
      from abjad.tools import componenttools
      from abjad.tools import spannertools
      assert componenttools.all_are_components(components)
      insert_offset = self.offset.stop
      receipt = spannertools.get_spanners_that_dominate_components([self])
      for spanner, index in receipt:
         insert_component = spannertools.find_spanner_component_starting_at_exactly_score_offset(
            spanner, insert_offset)
         if insert_component is not None:
            insert_index = spanner.index(insert_component)
         else:
            insert_index = len(spanner)
         for component in reversed(components):
            spanner._insert(insert_index, component)
            #component.spanners._add(spanner)
            component._spanners.add(spanner)
      parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([self])
      if parent is not None:
         for component in reversed(components):
            component.parentage._switch(parent)
            parent._music.insert(start + 1, component)
      return [self] + components

   def splice_left(self, components):
      '''Splice `components` before `self`.
      Extend spanners leftwards to attach to all components in list.'''
      from abjad.tools import componenttools
      from abjad.tools import componenttools
      from abjad.tools import spannertools
      assert componenttools.all_are_components(components)
      offset = self.offset.start
      receipt = spannertools.get_spanners_that_dominate_components([self])
      for spanner, x in receipt:
         index = spannertools.find_index_of_spanner_component_at_score_offset(spanner, offset)
         for component in reversed(components):
            spanner._insert(index, component)
            #component.spanners._add(spanner)
            component._spanners.add(spanner)
      parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([self])
      if parent is not None:
         for component in reversed(components):
            component.parentage._switch(parent)
            parent._music.insert(start, component)
      return components + [self] 

   ## MANGLED METHODS ##

   def __update_explicit_meters_of_entire_score_tree(self):
      from abjad.tools import componenttools
      from abjad.tools import measuretools
      #print 'updating all explicit meters in score (from %s) ...' % str(self.__class__.__name__)
      total_components_iterated = 0
      score = self.parentage.root
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
      score = self.parentage.root
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
      score = self.parentage.root
      components = componenttools.iterate_components_depth_first(score, 
         capped = True, unique = True, forbid = None, direction = 'left')
      for component in components:
         #print '\tnow updating %s offset values in seconds ...' % str(component.__class__.__name__)
         component.offset._update_offset_values_of_component_in_seconds( )
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
      score = self.parentage.root
      components = componenttools.iterate_components_depth_first(score, 
         capped = True, unique = True, forbid = None, direction = 'left')
      for component in components:
         component.offset._update_prolated_offset_values_of_component( )
         component._prolated_offset_values_are_current = True
         total_components_iterated += 1
      #print total_components_iterated, '... prolated offset values updated.'

   ## PRIVATE UPDATE METHODS ##

   def _mark_entire_score_tree_for_later_update(self, value):
      '''Call immediately AFTER MODIFYING score tree.
      '''
      assert value in ('prolated', 'marks', 'seconds')
      for component in self.parentage.improper_parentage:
         if value == 'prolated':
            component._prolated_offset_values_are_current = False
         elif value == 'marks':
            component._marks_are_current = False
         elif value == 'seconds':
            component._offset_values_of_in_seconds_are_current = False
         else:
            raise ValueError

   def _get_score_tree_state_flags(self):
      prolated_offset_values_are_current = True
      marks_are_current = True
      offset_values_in_seconds_are_current = True
      for component in self.parentage.improper_parentage:
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
