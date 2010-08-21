from abjad.core import _Abjad
from abjad.core import _Navigator
from abjad.core import LilyPondContextSettingComponentPlugIn
from abjad.core import LilyPondGrobOverrideComponentPlugIn
from abjad.core import LilyPondMiscellaneousCommandComponentPlugIn
from abjad.interfaces import _UpdateInterface
from abjad.interfaces import BreaksInterface
from abjad.interfaces import CommentsInterface
from abjad.interfaces import ClefInterface
from abjad.interfaces import DirectivesInterface
#from abjad.interfaces import DynamicsInterface
from abjad.interfaces import HistoryInterface
from abjad.interfaces import InterfaceAggregator
from abjad.interfaces import KeySignatureInterface
from abjad.interfaces import MeterInterface
from abjad.interfaces import NumberingInterface
from abjad.interfaces import OffsetInterface
from abjad.interfaces import ParentageInterface
from abjad.interfaces import StaffInterface
from abjad.interfaces import TempoInterface


class _Component(_Abjad):

   def __init__(self):
      self._interfaces = InterfaceAggregator(self)
      #self._breaks = BreaksInterface(self)
      #self._comments = CommentsInterface( )
      #self._directives = DirectivesInterface(self)
      #self._dynamics = DynamicsInterface(self)
      #self._history = HistoryInterface(self)
      self._lily_file = None
      #self._misc = LilyPondMiscellaneousCommandComponentPlugIn( )
      self._name = None
      self._navigator = _Navigator(self)
      #self._override = LilyPondGrobOverrideComponentPlugIn( )
      self._parentage = ParentageInterface(self)
      self._spanners = set([ ])
      #self._set = LilyPondContextSettingComponentPlugIn( )
      self._update = _UpdateInterface(self)

      ## Observer Interfaces must instantiate after _UpdateInterface ##
      self._clef = ClefInterface(self, self._update) ## TODO: weird backtracking conflict
      #self._key_signature = KeySignatureInterface(self, self._update)
      self._meter = MeterInterface(self, self._update) ## TODO: weird backtracking conflict
      self._numbering = NumberingInterface(self, self._update) ## no public access
      self._offset = OffsetInterface(self, self._update)
      self._staff = StaffInterface(self, self._update) ## TODO: weird backtracking conflict
      self._tempo = TempoInterface(self, self._update) ## TODO: weird backtracking conflict

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
         self._clef = ClefInterface(self, self._update)
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

#   @property
#   def dynamics(self):
#      '''Read-only reference to
#      :class:`~abjad.interfaces.dynamics.interface.DynamicsInterface`.'''
#      if not hasattr(self, '_dynamics'):
#         self._dynamics = DynamicsInterface(self)
#      return self._dynamics

   @property
   def format(self):
      '''Read-only version of `self` as LilyPond input code.'''
      return self._formatter.format

   @property
   def history(self):
      '''Read-only reference to 
      :class:`~abjad.interfaces.history.interface.HistoryInterface`.'''
      if not hasattr(self, '_history'):
         self._history = HistoryInterface(self)
      return self._history

   @property
   def interfaces(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.interface_aggregator.aggregator.InterfaceAggregator`.'''
      return self._interfaces

   @property
   def key_signature(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.key_signature.interface.KeySignatureInterface.`
      '''
      if not hasattr(self, '_key_signature'):
         self._key_signature = KeySignatureInterface(self, self._update)
      return self._key_signature

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
   def meter(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.meter.interface.MeterInterface`.''' 
      #if not hasattr(self, '_meter'):
      #   self._meter = MeterInterface(self, self._update)
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
         self._staff = StaffInterface(self, self._update)
      return self._staff

   @property
   def tempo(self):
      '''Read-only reference to
      :class:`~abjad.interfaces.tempo.interface.TempoInterface`.'''
      if not hasattr(self, '_tempo'):
         self._tempo = TempoInterface(self, self._update)
      return self._tempo

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
      insert_offset = self.offset.prolated.stop
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
      offset = self.offset.prolated.start
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
