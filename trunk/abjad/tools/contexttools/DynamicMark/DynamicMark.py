from abjad.tools.contexttools.ContextMark import ContextMark


class DynamicMark(ContextMark):
   '''.. versionadded:: 1.1.2

   Abjad model of a dynamic mark::

      abjad> contexttools.DynamicMark('f')
      DynamicMark('f')
   '''

   _format_slot = 'right'

   def __init__(self, dynamic_name_string, target_context = None):
      from abjad.components import Staff
      ContextMark.__init__(self, target_context = target_context)
      if self.target_context is None:
         self._target_context = Staff
      self._dynamic_name_string = dynamic_name_string

   ## OVERLOADS ##

   def __call__(self, *args):
      from abjad.exceptions import WellFormednessError
      from abjad.tools import spannertools
      if len(args) == 1:
         dynamic_spanners = \
            spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(
            args[0], klass = (spannertools.DynamicTextSpanner, spannertools.HairpinSpanner))
         for dynamic_spanner in dynamic_spanners:
            if not dynamic_spanner._is_exterior_leaf(args[0]):
               raise WellFormednessError(
                  '\n\tCan not attach dynamic mark to interior component of dynamic spanner.')
      return ContextMark.__call__(self, *args)

   def __copy__(self, *args):
      return type(self)(self._dynamic_name_string, target_contex = self.target_context)

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self._dynamic_name_string == arg._dynamic_name_string
      return False

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents_repr_string(self):
      return repr(self._dynamic_name_string)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      '''Read-only LilyPond input format of dynamic mark:

      ::

         abjad> dynamic_mark = contexttools.DynamicMark('f')
         abjad> dynamic_mark.format
         '\\f'
      '''
      return r'\%s' % self._dynamic_name_string
