from abjad.components._Component import _Component
from abjad.components._Context import _Context
from fractions import Fraction


class Mark(object):
   '''.. versionadded:: 1.1.2

   'Here forward' mark.

   Mark models time signatures, key signatures, clef, dynamics
   and other score symbols that establish a score setting to remain
   in effect until the next occurrence of such a score symbol.
   '''

   __slots__ = ('_effective_context', '_start_component', '_target_context', 'value')

   def __init__(self, value = None):
      self._contents_repr_string = ' '
      self._effective_context = None
      self._start_component = None
      self._target_context = None
      ## TODO: make mark value read-only
      self.value = value

   ## OVERLOADS ##

   def __call__(self, *args):
      if len(args) == 0:
         target_context = None
         start_component = None
      elif len(args) == 1:
         target_context = args[0]
         start_component = args[0]
      elif len(args) == 2:
         target_context = args[0]
         start_component = args[1]
      else:
         raise ValueError('must call mark with 0, 1 or 2 arguments only.')
      if not isinstance(target_context, (_Context, type(_Context), str, type(None))):
         raise TypeError(
            'mark target context "%s" must be context or context name.' % target_context)
      if start_component is not None:
         if not isinstance(start_component, _Component):
            raise TypeError('mark start component "%s" must be component.' % start_component)
      if isinstance(target_context, _Context):
         target_context = type(target_context)
      self._bind_start_component(start_component)
      self._target_context = target_context
      self._bind_effective_context(target_context)
      return self

   def __copy__(self, *args):
      new = type(self)(self.value)
      new._target_context = self._target_context
      return new

   __deepcopy__ = __copy__
      
   def __delattr__(self, *args):
      raise AttributeError('can not delete %s attributes.' % self.__class__.__name__)

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.value == arg.value:
            return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)%s' % (
         self.__class__.__name__, self._contents_repr_string, self._attachment_repr_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _attachment_repr_string(self):
      result = ''
      if self.start_component is not None:
         result += '*'
      if self.effective_context is not None:
         result += '*'
      return result

   @property
   def _is_fully_attached(self):
      return bool(self._start_component) and bool(self._effective_context)

   ## PRIVATE METHODS ##
   
   def _bind_effective_context(self, target_context):
      self._unbind_effective_context( )
      effective_context = self._find_effective_context(target_context)
      if effective_context is not None:
         effective_context._marks_for_which_component_functions_as_mark_context.append(self)
         effective_context._update._mark_all_improper_parents_for_update( )
      self._effective_context = effective_context

   def _bind_start_component(self, start_component):
      self._unbind_start_component( )
      if start_component is not None:
         start_component._marks_for_which_component_functions_as_start_component.append(self)
         start_component._update._mark_all_improper_parents_for_update( )
      self._start_component = start_component

   def _find_effective_context(self, target_context):
      if target_context is None:
         return None
      elif isinstance(target_context, type):
         target_context_type = target_context
         for component in self.start_component.parentage.improper_parentage:
            if isinstance(component, target_context_type):
               return component
      elif isinstance(target_context, str):
         target_context_name = target_context
         for component in self.start_component.parentage.improper_parentage:
            if component.name == target_context_name:
               return component
      else:
         raise TypeError('target context "%s" must be context type, context name or none.' % 
            target_context)

   def _unbind_effective_context(self):
      effective_context = self._effective_context
      if effective_context is not None:
         try:
            effective_context._marks_for_which_component_functions_as_mark_context.remove(self)
         except ValueError:
            pass
      self._effective_context = None

   def _unbind_start_component(self):
      start_component = self._start_component
      if start_component is not None:
         try:
            start_component._marks_for_which_component_functions_as_start_component.remove(self)
         except ValueError:
            pass
      self._start_component = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective_context(self):
      if self.start_component is not None:
         update_interface = self.start_component._update
         if not update_interface._prolated_offset_values_of_all_improper_parents_are_current:
            update_interface._update_prolated_offset_values_of_all_score_components( )
         if not update_interface._any_improper_parents_are_currently_updating:
            if not update_interface._all_improper_parents_are_current:
               update_interface._update_observer_interfaces_of_all_score_components( )
         return self._effective_context

   @property
   def start_component(self):
      return self._start_component

   @property
   def target_context(self):
      return self._target_context

   ## PUBLIC METHODS ##

   def attach_mark(self, context, start_component):
      return self(context, start_component)

   ## TODO: rename to detach_mark( ) ##
   def detach_mark_from_context_and_start_component(self):
      return self( )

   def detach_mark(self):
      return self( )
