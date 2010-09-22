from abjad.components._Component import _Component
from abjad.components._Context import _Context
from fractions import Fraction


## TODO: how to test _Context subtypes like Staff? ##
class Mark(object):
   '''.. versionadded:: 1.1.2

   Mark models time signatures, key signatures, clef, dynamics
   and other score symbols that establish a score setting to remain
   in effect until the next occurrence of such a score symbol.
   '''

   __slots__ = ('_contents_repr_string', '_effective_context', '_start_component', 
      '_target_context')

   def __init__(self, target_context = None):
      self._contents_repr_string = ' '
      self._effective_context = None
      self._start_component = None
      if target_context is not None:
         if not isinstance(target_context, type):
            raise TypeError('target context "%s" must be context class.' % target_context)
      self._target_context = target_context

   ## OVERLOADS ##

   def __call__(self, *args):
      if len(args) == 0:
         return self.detach_mark( )
      elif len(args) == 1:
         return self.attach_mark(args[0])
      else:
         raise ValueError('must call mark with at most 1 argument.')

   def __copy__(self, *args):
      return type(self)(target_context = self._target_context)

   __deepcopy__ = __copy__
      
   def __delattr__(self, *args):
      raise AttributeError('can not delete %s attributes.' % self.__class__.__name__)

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
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
      if self.start_component is None:
         return ''
      else:
         return '(%s)' % str(self.start_component)

   ## MANGLED METHODS ##

   def __bind_correct_effective_context(self, correct_effective_context):
      self.__unbind_effective_context( )
      if correct_effective_context is not None:
         correct_effective_context._marks_for_which_component_functions_as_effective_context.append(
            self)
      self._effective_context = correct_effective_context
      correct_effective_context._mark_entire_score_tree_for_later_update('marks')

   def __bind_start_component(self, start_component):
      assert isinstance(start_component, _Component)
      self.__unbind_start_component( )
      start_component._marks_for_which_component_functions_as_start_component.append(self)
      self._start_component = start_component
      self._start_component._mark_entire_score_tree_for_later_update('marks')

   def __unbind_effective_context(self):
      effective_context = self._effective_context
      if effective_context is not None:
         try:
            effective_context._marks_for_which_component_functions_as_effective_context.remove(self)
         except ValueError:
            pass
      self._effective_context = None

   def __unbind_start_component(self):
      start_component = self._start_component
      if start_component is not None:
         try:
            start_component._marks_for_which_component_functions_as_start_component.remove(self)
         except ValueError:
            pass
      self._start_component = None

   ## PRIVATE METHODS ##
   
   def _find_correct_effective_context(self):
      from abjad.tools import componenttools
      target_context = self.target_context
      if target_context is None:
         return None
      elif isinstance(target_context, type):
         target_context_type = target_context
         #for component in self.start_component.parentage.improper_parentage:
         for component in componenttools.get_improper_parentage_of_component(self.start_component):
            if isinstance(component, target_context_type):
               return component
      elif isinstance(target_context, str):
         target_context_name = target_context
         #for component in self.start_component.parentage.improper_parentage:
         for component in componenttools.get_improper_parentage_of_component(self.start_component):
            if component.name == target_context_name:
               return component
      else:
         raise TypeError('target context "%s" must be context type, context name or none.' % 
            target_context)

   def _update_effective_context(self):
      '''This function is designed to be called by score components during score update.
      '''
      current_effective_context = self._effective_context
      correct_effective_context = self._find_correct_effective_context( )
      if current_effective_context is not correct_effective_context:
         self.__bind_correct_effective_context(correct_effective_context)

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective_context(self):
      if self.start_component is not None:
         self.start_component._update_marks_of_entire_score_tree_if_necessary( )
      return self._effective_context

   @property
   def start_component(self):
      return self._start_component

   @property
   def target_context(self):
      return self._target_context

   ## PUBLIC METHODS ##

   def attach_mark(self, start_component):
      self.__bind_start_component(start_component)
      return self

   def detach_mark(self):
      self.__unbind_start_component( )
      self.__unbind_effective_context( )
      return self
